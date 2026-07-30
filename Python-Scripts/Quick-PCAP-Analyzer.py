#!/usr/bin/env python3                                                             
#                                                                                                   #
# Name: pcap_analyzer.py                                                                            #
# Description: A PCAP/PCAPNG analyzer for defensive cybersecurity research and CTF triage.          #
#              Produced a beautiful colored output with insights of the caputre                     #
# PURPOSE:                                                                                          #
#   Parse raw packet capture files (classic .pcap and .pcapng formats) using only                   #
#   the Python standard library. Extract protocol hierarchies, DNS queries/responses,               #
#   HTTP transactions, TLS ClientHello metadata, cleartext credentials, and network                 #
#   anomalies. Output a structured report to stdout (table or JSON).                                #
#                                                                                                   #
# DESIGN:                                                                                           #
#   - Zero third-party dependencies. Runs on any Python 3.7+ installation.                          #
#   - Read-only analysis. Never modifies the input file.                                            #
#   - Secrets are redacted by default (--reveal-secrets to override).                               #
#   - Bounded memory: event lists are capped at --limit entries per section.                        #
#                                                                                                   #
# ARCHITECTURE (data flow):                                                                         #
#   File on disk                                                                                    #
#     -> iter_packets()        : detect format, yield (ts, caplen, origlen, raw_bytes, linktype)    #
#       -> parse_packet()      : decode L2/L3/L4 into a ParsedPacket dataclass                      #
#         -> Analyzer.process_packet() : dispatch to protocol handlers, accumulate stats            #
#           -> Analyzer.report()       : serialize accumulated state to a dict                      #
#             -> print_report() / JSON : render to stdout                                           #
#                                                                                                   #
# Author: Maat from https://github.com/Maat-Cyber/Maat-Cyber-World                                  #
# ###################################################################################################



from __future__ import annotations

import argparse
import base64
import gzip
import json
import math
import os
import socket
import struct
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import parse_qsl


# ---------------------------------------------------------------------------
# Feature flags: each corresponds to a section of the analysis report.
# Users can enable/disable subsets via --only / --skip / --interactive.
# ---------------------------------------------------------------------------
FEATURES = [
    "summary",       # File metadata, packet counts, time span
    "protocols",     # IP version, transport protocol, port, and TCP flag distributions
    "conversations", # Top talker pairs by byte volume
    "dns",           # DNS query/response extraction and suspicious-name heuristics
    "http",          # HTTP request/response parsing (cleartext only)
    "tls",           # TLS ClientHello SNI and version extraction
    "creds",         # Credential harvesting: HTTP Basic, cookies, form fields, FTP
    "anomalies",     # Scan detection (NULL, XMAS, SYN-FIN), large ICMP, suspicious URIs
]

# ---------------------------------------------------------------------------
# Link-layer type constants (from the pcap "network" field or pcapng IDB).
# Only the most common types are handled; unknown types cause the packet
# to be silently skipped (parse_packet returns an empty ParsedPacket).
# ---------------------------------------------------------------------------
LINKTYPES = {
    0: "NULL/LOOPBACK",   # BSD loopback: 4-byte address-family header
    1: "ETHERNET",        # Standard Ethernet II framing (most common)
    101: "RAW",           # Raw IP: no L2 header, first nibble is IP version
    113: "LINUX_SLL",     # Linux "cooked" capture (tcpdump -i any)
}

# ---------------------------------------------------------------------------
# IANA IP protocol numbers used for labeling in reports.
# Reference: https://www.iana.org/assignments/protocol-numbers/
# ---------------------------------------------------------------------------
IP_PROTOS = {
    1: "ICMP",
    2: "IGMP",
    6: "TCP",
    17: "UDP",
    41: "IPv6",       # IPv6-in-IPv4 tunneling
    47: "GRE",
    50: "ESP",        # IPsec Encapsulating Security Payload
    51: "AH",         # IPsec Authentication Header
    58: "ICMPv6",
    89: "OSPF",
    132: "SCTP",
}

# ---------------------------------------------------------------------------
# TCP flag bitmasks. Used both for counting flag occurrences in the
# "protocols" section and for anomaly detection (scan signatures).
# Reference: RFC 9293 (TCP), RFC 3168 (ECN: ECE/CWR).
# ---------------------------------------------------------------------------
TCP_FLAG_NAMES = {
    "FIN": 0x01,
    "SYN": 0x02,
    "RST": 0x04,
    "PSH": 0x08,
    "ACK": 0x10,
    "URG": 0x20,
    "ECE": 0x40,   # ECN-Echo
    "CWR": 0x80,   # Congestion Window Reduced
}

# ---------------------------------------------------------------------------
# DNS record type codes for human-readable labels.
# Reference: IANA DNS Parameters registry.
# ---------------------------------------------------------------------------
DNS_TYPES = {
    1: "A",
    2: "NS",
    5: "CNAME",
    6: "SOA",
    12: "PTR",
    15: "MX",
    16: "TXT",
    28: "AAAA",
    33: "SRV",
    65: "HTTPS",    # SVCB/HTTPS RR (RFC 9460)
    257: "CAA",
}

# ---------------------------------------------------------------------------
# Valid HTTP/1.x request methods (as raw bytes for zero-copy prefix checks).
# Used by looks_http() to decide whether a TCP payload is HTTP.
# Reference: RFC 9110 Section 9.
# ---------------------------------------------------------------------------
HTTP_METHODS_BYTES = {
    b"OPTIONS",
    b"GET",
    b"HEAD",
    b"POST",
    b"PUT",
    b"DELETE",
    b"TRACE",
    b"CONNECT",
    b"PATCH",
}

# ---------------------------------------------------------------------------
# Substrings that, when found in an HTTP form field name or query parameter,
# suggest the field carries a secret value (password, token, API key, etc.).
# Used by is_secret_field() for credential extraction.
# ---------------------------------------------------------------------------
SECRET_FIELD_PATTERNS = (
    "pass",
    "pwd",
    "passwd",
    "secret",
    "token",
    "api",
    "key",
    "auth",
    "private",
    "credential",
)


# ===========================================================================
# Terminal color helper.
# Respects the NO_COLOR convention (https://no-color.org/) and auto-disables
# when stdout is not a TTY or when --json / --no-color is passed.
# ===========================================================================
class Painter:
    # ANSI SGR escape sequences for the subset of styles we use.
    STYLES = {
        "bold": "\033[1m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "grey": "\033[90m",
    }
    RESET = "\033[0m"

    def __init__(self, enabled: bool):
        self.enabled = enabled

    def paint(self, text: str, *styles: str) -> str:
        """Wrap *text* in ANSI codes if coloring is enabled; otherwise return as-is."""
        if not self.enabled:
            return text
        prefix = "".join(self.STYLES[s] for s in styles if s in self.STYLES)
        if not prefix:
            return text
        return f"{prefix}{text}{self.RESET}"


# ===========================================================================
# ASCII table renderer.
# Produces a bordered table with auto-sized columns.  Optional per-row
# colors let callers highlight warnings (yellow) or critical findings (red).
# ===========================================================================
def render_table(painter, headers, rows, row_colors=None):
    rows = list(rows)
    if not rows:
        return painter.paint("No data.", "grey")

    # Convert every cell to str and truncate to header count.
    str_rows = [[str(x) for x in row][:len(headers)] for row in rows]
    # Pad short rows so every row has exactly len(headers) cells.
    for row in str_rows:
        while len(row) < len(headers):
            row.append("")

    # Compute the maximum display width for each column.
    widths = [len(str(h)) for h in headers]
    for row in str_rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))

    # Horizontal separator line, e.g. +------+--------+
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    lines = [painter.paint(sep, "grey")]

    # Header row (bold cyan).
    header_cells = []
    for i, h in enumerate(headers):
        header_cells.append(painter.paint(str(h).ljust(widths[i]), "bold", "cyan"))
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append(painter.paint(sep, "grey"))

    # Data rows, optionally colored per-row.
    for r_idx, row in enumerate(str_rows):
        color = None
        if row_colors and r_idx < len(row_colors):
            color = row_colors[r_idx]

        cells = []
        for i, cell in enumerate(row):
            padded = cell.ljust(widths[i])
            if color:
                cells.append(painter.paint(padded, color))
            else:
                cells.append(padded)
        lines.append("| " + " | ".join(cells) + " |")

    lines.append(painter.paint(sep, "grey"))
    return "\n".join(lines)


def print_section(painter, title, content, title_color="cyan"):
    """Print a titled block: blank line, === TITLE ===, then content."""
    print()
    print(painter.paint(f"=== {title} ===", "bold", title_color))
    print(content)


def print_banner(painter, title):
    """Print a centered banner used at the top of the report."""
    bar = "=" * (len(title) + 4)
    print()
    print(painter.paint(bar, "cyan"))
    print(painter.paint(f"  {title}", "bold", "cyan"))
    print(painter.paint(bar, "cyan"))


def human_bytes(n):
    """Format a byte count into a human-readable string (e.g. '1.5 MB')."""
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(n)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} B"
            return f"{value:.1f} {unit}"
        value /= 1024


def ts_to_str(ts):
    """Convert a Unix timestamp (float seconds) to a UTC string, or 'N/A'."""
    if ts is None:
        return "N/A"
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        # Trim microseconds to milliseconds for readability.
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"
    except Exception:
        return f"{ts:.6f}"


def shannon_entropy(s):
    """
    Compute Shannon entropy (bits per character) of a string.
    Used as a heuristic for detecting DGA / tunneling domain names:
    random-looking strings have entropy approaching log2(alphabet_size).
    """
    if not s:
        return 0.0
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    entropy = 0.0
    length = len(s)
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def u16be(data, off):
    """Read an unsigned 16-bit big-endian integer from *data* at *off*."""
    return struct.unpack_from(">H", data, off)[0]


def ipv4_checksum(header_bytes):
    """
    Compute the IPv4 header checksum (RFC 791 Section 3.1).
    The checksum field in the header must be zeroed before calling this.
    Algorithm: one's-complement sum of 16-bit words, then complement.
    """
    if len(header_bytes) % 2:
        header_bytes += b"\x00"  # Pad to even length if necessary.
    s = sum(struct.unpack(f"!{len(header_bytes)//2}H", header_bytes))
    # Fold 32-bit accumulator into 16 bits.
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF


# ===========================================================================
# DNS name decoder.
# Handles label sequences and compression pointers (RFC 1035 Section 4.1.4).
# A set of visited offsets prevents infinite loops on malformed/circular pointers.
# Returns (decoded_name, next_offset_after_name).
# ===========================================================================
def decode_dns_name(data, offset):
    labels = []
    jumped = False          # True once we follow a compression pointer.
    next_offset = None      # The offset to resume from after the first pointer.
    seen = set()            # Visited offsets to detect circular pointers.

    while True:
        if offset >= len(data):
            break
        if offset in seen:  # Circular pointer guard.
            break
        seen.add(offset)

        length = data[offset]
        if length == 0:     # Root label: end of name.
            offset += 1
            break

        # Compression pointer: top two bits are 11 (0xC0).
        # The remaining 14 bits are an offset into the DNS message.
        if (length & 0xC0) == 0xC0:
            if offset + 1 >= len(data):
                break
            pointer = ((length & 0x3F) << 8) | data[offset + 1]
            if not jumped:
                # Remember where to continue after the pointer (2-byte pointer field).
                next_offset = offset + 2
                jumped = True
            offset = pointer
            continue

        # Normal label: 1 length byte followed by that many octets.
        offset += 1
        if offset + length > len(data):
            break

        labels.append(data[offset:offset + length].decode("utf-8", "replace"))
        offset += length

    name = ".".join(labels) or "."
    return name, next_offset if jumped else offset


# ===========================================================================
# DNS message parser (RFC 1035).
# Handles both UDP (bare message) and TCP (2-byte length prefix) transports.
# Extracts the header fields, question section, and answer section.
# Authority and additional sections are counted but not parsed (not needed
# for triage-level analysis).
# ===========================================================================
def parse_dns(payload, tcp=False):
    # TCP DNS messages are prefixed with a 2-byte length field (RFC 1035 §4.2.2).
    if tcp:
        if len(payload) < 2:
            return None
        dns_len = u16be(payload, 0)
        payload = payload[2:]
        if dns_len < len(payload):
            payload = payload[:dns_len]

    # Minimum DNS header is 12 bytes: ID(2) FLAGS(2) QD(2) AN(2) NS(2) AR(2).
    if len(payload) < 12:
        return None

    tx_id, flags, qdcount, ancount, nscount, arcount = struct.unpack_from(">HHHHHH", payload, 0)
    qr = (flags >> 15) & 1          # 0 = query, 1 = response
    opcode = (flags >> 11) & 0xF    # 0 = QUERY, 1 = IQUERY, 2 = STATUS, ...
    rcode = flags & 0xF             # 0 = NoError, 3 = NXDOMAIN, ...

    # --- Question section ---
    off = 12
    questions = []
    for _ in range(min(qdcount, 20)):  # Cap to avoid pathological loops.
        name, off = decode_dns_name(payload, off)
        if off + 4 > len(payload):
            break
        qtype = u16be(payload, off)
        qclass = u16be(payload, off + 2)
        off += 4
        questions.append({
            "name": name,
            "type": DNS_TYPES.get(qtype, str(qtype)),
            "class": qclass,
        })

    # --- Answer section ---
    answers = []
    for _ in range(min(ancount, 50)):  # Cap to avoid pathological loops.
        name, off = decode_dns_name(payload, off)
        if off + 10 > len(payload):
            break

        # RR fixed fields: TYPE(2) CLASS(2) TTL(4) RDLENGTH(2).
        rtype, rclass, ttl, rdlen = struct.unpack_from(">HHIH", payload, off)
        off += 10

        if off + rdlen > len(payload):
            break

        # Decode RDATA based on record type.
        rdata = ""
        if rtype == 1 and rdlen == 4:
            # A record: 4-byte IPv4 address.
            rdata = socket.inet_ntop(socket.AF_INET, payload[off:off + 4])
        elif rtype == 28 and rdlen == 16:
            # AAAA record: 16-byte IPv6 address.
            rdata = socket.inet_ntop(socket.AF_INET6, payload[off:off + 16])
        elif rtype in (2, 5, 12):
            # NS, CNAME, PTR: RDATA is a domain name.
            rdata, _ = decode_dns_name(payload, off)
        elif rtype == 15 and rdlen >= 3:
            # MX record: 2-byte preference + domain name.
            pref = u16be(payload, off)
            exch, _ = decode_dns_name(payload, off + 2)
            rdata = f"{pref} {exch}"
        elif rtype == 16:
            # TXT record: one or more <length><character-string> pairs.
            txt_off = off
            end = off + rdlen
            parts = []
            while txt_off < end:
                tlen = payload[txt_off]
                txt_off += 1
                if txt_off + tlen > end:
                    break
                parts.append(payload[txt_off:txt_off + tlen].decode("utf-8", "replace"))
                txt_off += tlen
            rdata = " | ".join(parts)
        else:
            # Fallback: hex-encode the first 16 bytes of RDATA.
            rdata = payload[off:off + min(rdlen, 16)].hex()

        off += rdlen
        answers.append({
            "name": name,
            "type": DNS_TYPES.get(rtype, str(rtype)),
            "class": rclass,
            "ttl": ttl,
            "data": rdata,
        })

    return {
        "id": tx_id,
        "qr": qr,
        "opcode": opcode,
        "rcode": rcode,
        "questions": questions,
        "answers": answers,
    }


# ===========================================================================
# HTTP detection heuristic.
# Returns True if the payload *looks like* an HTTP/1.x message.
# Checks: known method prefix, "HTTP/" response prefix, or well-known port
# combined with HTTP-like content in the first 200 bytes.
# This is intentionally conservative to avoid false positives on binary streams.
# ===========================================================================
def looks_http(payload, sport, dport):
    if not payload:
        return False

    # Check for a request line: "GET /path HTTP/1.1"
    for method in HTTP_METHODS_BYTES:
        if payload.startswith(method + b" "):
            return True

    # Check for a response status line: "HTTP/1.1 200 OK"
    if payload.startswith(b"HTTP/"):
        return True

    # Port-based heuristic for captures where the payload starts mid-stream
    # or where the method is not at byte 0 (e.g. pipelined requests).
    if 80 in (sport, dport) or 8080 in (sport, dport) or 8000 in (sport, dport) or 8888 in (sport, dport):
        head = payload[:200]
        if b"HTTP/" in head or b"Host:" in head:
            return True

    return False


# ===========================================================================
# HTTP/1.x message parser.
# Extracts the start line (method+URI or status+reason), headers, and
# URL-encoded form body fields.  Only the first 100 KB of payload is
# examined to bound memory usage on large transfers.
# ===========================================================================
def parse_http(payload):
    if not payload:
        return None

    # Cap the inspected region to 100 KB.
    data = payload[:100000]

    # Locate the header/body boundary.  HTTP/1.x uses CRLF, but some
    # non-conformant implementations use bare LF.
    header_end = data.find(b"\r\n\r\n")
    if header_end != -1:
        header_bytes = data[:header_end]
        body = data[header_end + 4:]
        line_sep = b"\r\n"
    else:
        header_end = data.find(b"\n\n")
        if header_end != -1:
            header_bytes = data[:header_end]
            body = data[header_end + 2:]
            line_sep = b"\n"
        else:
            # No blank line found: treat entire payload as headers (no body).
            header_bytes = data
            body = b""
            line_sep = b"\r\n" if b"\r\n" in data else b"\n"

    if not header_bytes:
        return None

    lines = header_bytes.split(line_sep)
    if not lines:
        return None

    # First line is the start line.  Decode as latin-1 to preserve raw bytes.
    start = lines[0].decode("latin-1", "replace")
    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        text = line.decode("latin-1", "replace")
        if ":" in text:
            k, v = text.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    event = {"headers": headers}
    method = start.split(" ", 1)[0].encode("latin-1", "replace")

    if method in HTTP_METHODS_BYTES:
        # Request line: "METHOD /uri HTTP/x.y"
        parts = start.split(" ")
        if len(parts) < 3:
            return None
        event["kind"] = "request"
        event["method"] = parts[0]
        event["uri"] = parts[1]
        event["version"] = parts[2]
        host = headers.get("host", "")
        event["host"] = host
        # Reconstruct an absolute URL when possible.
        if host and event["uri"].startswith("/"):
            event["url"] = f"http://{host}{event['uri']}"
        else:
            event["url"] = event["uri"]
    elif start.startswith("HTTP/"):
        # Status line: "HTTP/x.y 200 OK"
        parts = start.split(" ", 2)
        if len(parts) < 2:
            return None
        event["kind"] = "response"
        event["version"] = parts[0]
        try:
            event["status"] = int(parts[1])
        except ValueError:
            event["status"] = 0
        event["reason"] = parts[2] if len(parts) > 2 else ""
    else:
        # Not a recognizable HTTP start line.
        return None

    # If the body is URL-encoded form data, parse the fields.
    # This is where login credentials often appear in cleartext captures.
    content_type = headers.get("content-type", "").lower()
    if body and "application/x-www-form-urlencoded" in content_type:
        try:
            fields = parse_qsl(body.decode("utf-8", "replace"), keep_blank_values=True)
            event["form_fields"] = [{"name": k, "value": v} for k, v in fields[:100]]
        except Exception:
            event["form_fields"] = []

    return event


def is_tls(payload):
    """
    Quick check: TLS record layer starts with content-type 0x16 (Handshake).
    This is necessary but not sufficient; parse_tls() does full validation.
    """
    return bool(payload) and len(payload) >= 6 and payload[0] == 0x16


# ===========================================================================
# TLS ClientHello parser (RFC 8446 / RFC 5246).
# Extracts: record version, handshake client version, SNI (server_name
# extension, type 0x0000), and cipher suite count.
# Only ClientHello (handshake type 1) is parsed; other handshake messages
# and non-handshake records return None.
# ===========================================================================
def parse_tls(payload):
    if not is_tls(payload):
        return None

    # TLS record header: ContentType(1) ProtocolVersion(2) Length(2).
    record_version = u16be(payload, 1)
    record_len = u16be(payload, 3)

    # Extract the handshake message from the record.
    if 5 + record_len <= len(payload):
        hs = payload[5:5 + record_len]
    else:
        hs = payload[5:]  # Truncated record; parse what we have.

    # Handshake header: HandshakeType(1) Length(3).
    # Type 1 = ClientHello.
    if len(hs) < 4 or hs[0] != 1:
        return None

    hs_len = int.from_bytes(hs[1:4], "big")
    if 4 + hs_len <= len(hs):
        body = hs[4:4 + hs_len]
    else:
        body = hs[4:]

    # ClientHello minimum: version(2) + random(32) + session_id_len(1) = 35 bytes.
    if len(body) < 34:
        return None

    off = 0
    # Client version (e.g. 0x0303 = TLS 1.2, 0x0301 = TLS 1.0).
    client_version = u16be(body, off)
    off += 2
    # 32-byte random (gmt_unix_time + random_bytes). Skip it.
    off += 32

    # Session ID: 1-byte length prefix + variable data.
    if off >= len(body):
        return None
    sid_len = body[off]
    off += 1 + sid_len

    # Cipher suites: 2-byte total length + list of 2-byte suite IDs.
    if off + 2 > len(body):
        return None
    cipher_len = u16be(body, off)
    off += 2 + cipher_len

    # Compression methods: 1-byte count + list of 1-byte method IDs.
    if off >= len(body):
        return None
    comp_len = body[off]
    off += 1 + comp_len

    result = {
        "version": f"0x{client_version:04x}",
        "record_version": f"0x{record_version:04x}",
        "sni": None,
        "cipher_suites": cipher_len // 2,  # Each suite is 2 bytes.
    }

    # Extensions block (present in TLS 1.0+ ClientHello).
    if off + 2 > len(body):
        return result

    ext_len = u16be(body, off)
    off += 2
    end = off + ext_len
    if end > len(body):
        end = len(body)

    # Walk the extension list looking for SNI (type 0x0000).
    while off + 4 <= end:
        ext_type = u16be(body, off)
        ext_data_len = u16be(body, off + 2)
        off += 4

        if off + ext_data_len > end:
            break

        if ext_type == 0:
            # server_name extension (RFC 6066).
            # Structure: ServerNameListLength(2) NameType(1) NameLength(2) Name(...)
            sni_data = body[off:off + ext_data_len]
            if len(sni_data) >= 5:
                pos = 2  # Skip the 2-byte list length.
                name_type = sni_data[pos]
                name_len = u16be(sni_data, pos + 1)
                pos += 3
                if name_type == 0 and pos + name_len <= len(sni_data):
                    # name_type 0 = host_name.
                    result["sni"] = sni_data[pos:pos + name_len].decode("utf-8", "replace")

        off += ext_data_len

    return result


# ===========================================================================
# FTP control-channel parser.
# Recognizes USER and PASS commands (cleartext credential exposure)
# and numeric response codes.  Only the first line of the payload is
# examined, which is sufficient for command/response detection.
# ===========================================================================
def parse_ftp(payload):
    if not payload:
        return None

    # FTP uses CRLF line endings; fall back to LF.
    line = payload.split(b"\r\n", 1)[0].split(b"\n", 1)[0]
    text = line.decode("utf-8", "replace")
    if not text:
        return None

    upper = text.upper()
    if upper.startswith("USER "):
        return {"kind": "command", "command": "USER", "value": text[5:].strip()}
    if upper.startswith("PASS "):
        return {"kind": "command", "command": "PASS", "value": text[5:].strip()}
    # Server responses start with a 3-digit code (e.g. "230 Login successful").
    if text[:3].isdigit():
        return {"kind": "response", "code": int(text[:3]), "message": text[4:].strip()}

    return None


def cookie_names(header):
    """
    Extract cookie *names* (not values) from a Cookie or Set-Cookie header.
    Values are intentionally omitted to avoid leaking secrets into the report
    unless --reveal-secrets is used.  Returns at most 10 names.
    """
    names = []
    for cookie in header.split(","):
        first = cookie.split(";", 1)[0]
        if "=" in first:
            name = first.split("=", 1)[0].strip()
            if name:
                names.append(name)
    return names[:10]


def is_secret_field(name):
    """Return True if a form field name matches any known secret pattern."""
    n = name.lower()
    return any(p in n for p in SECRET_FIELD_PATTERNS)


# ===========================================================================
# ParsedPacket: the intermediate representation produced by parse_packet().
# Holds decoded L2/L3/L4 fields and the raw application-layer payload.
# Fields are Optional because not every packet has every layer
# (e.g. ARP has no IP header; ICMP has no ports).
# ===========================================================================
@dataclass
class ParsedPacket:
    eth_src: Optional[str] = None     # Source MAC address (Ethernet only)
    eth_dst: Optional[str] = None     # Destination MAC address (Ethernet only)
    vlan: Optional[int] = None        # 802.1Q VLAN ID, if present
    ip_ver: Optional[int] = None      # 4 or 6
    src: Optional[str] = None         # Source IP address (string)
    dst: Optional[str] = None         # Destination IP address (string)
    proto: Optional[int] = None       # IP protocol number (6=TCP, 17=UDP, ...)
    sport: Optional[int] = None       # Source port (TCP/UDP only)
    dport: Optional[int] = None       # Destination port (TCP/UDP only)
    tcp_flags: Optional[int] = None   # Raw TCP flags byte
    icmp_type: Optional[int] = None   # ICMP type field
    icmp_code: Optional[int] = None   # ICMP code field
    payload: bytes = b""              # Application-layer payload bytes
    ip_len: int = 0                   # Total IP packet length
    ttl: Optional[int] = None         # IPv4 TTL / IPv6 Hop Limit
    app: str = ""                     # Application protocol label (set by handlers)


# ===========================================================================
# Transport-layer parser.
# Dispatches on IP protocol number to decode TCP, UDP, or ICMP headers
# and extract the application payload into pp.payload.
# *end* marks the end of the IP packet (respects IP total_length).
# ===========================================================================
def parse_transport(proto, data, off, pp, end=None):
    if end is None or end > len(data):
        end = len(data)
    if off >= end:
        return

    if proto == 6:
        # --- TCP (RFC 9293) ---
        # Minimum TCP header is 20 bytes.
        if end < off + 20:
            return
        pp.sport = u16be(data, off)
        pp.dport = u16be(data, off + 2)
        # Data offset is in the high nibble of byte 12, in 32-bit words.
        data_offset = (data[off + 12] >> 4) * 4
        if data_offset < 20:
            data_offset = 20  # Enforce minimum; malformed packets exist.
        pp.tcp_flags = data[off + 13]  # Flags byte (FIN..CWR).
        payload_start = off + data_offset
        if payload_start < end:
            pp.payload = data[payload_start:end]
        else:
            pp.payload = b""

    elif proto == 17:
        # --- UDP (RFC 768) ---
        # UDP header is always 8 bytes: src(2) dst(2) len(2) checksum(2).
        if end < off + 8:
            return
        pp.sport = u16be(data, off)
        pp.dport = u16be(data, off + 2)
        udp_len = u16be(data, off + 4)
        payload_start = off + 8
        if udp_len >= 8:
            # Use the UDP length field to bound the payload, but never
            # exceed the IP packet boundary.
            payload_end = off + udp_len
            if payload_end > end:
                payload_end = end
        else:
            # Malformed length; fall back to IP boundary.
            payload_end = end
        if payload_start < payload_end:
            pp.payload = data[payload_start:payload_end]
        else:
            pp.payload = b""

    elif proto in (1, 58):
        # --- ICMP / ICMPv6 ---
        # Header: Type(1) Code(1) Checksum(2) + variable data.
        if end < off + 4:
            return
        pp.icmp_type = data[off]
        pp.icmp_code = data[off + 1]
        pp.payload = data[off + 4:end]  # Everything after the 4-byte header.


# ===========================================================================
# IPv4 parser (RFC 791).
# Decodes the fixed 20-byte header, handles IHL > 5 (IP options),
# and skips transport parsing for non-zero fragment offsets
# (only the first fragment carries the L4 header).
# ===========================================================================
def parse_ipv4(data, off, pp):
    if len(data) < off + 20:
        return

    vihl = data[off]
    version = vihl >> 4       # High nibble: must be 4.
    ihl = (vihl & 0x0F) * 4  # Low nibble: header length in 32-bit words.

    if version != 4 or ihl < 20 or len(data) < off + ihl:
        return

    total_len = u16be(data, off + 2)
    # Sanity: total_len must cover at least the header and not exceed
    # the available data.  Some captures have incorrect total_len.
    if total_len < ihl or total_len > len(data) - off:
        total_len = len(data) - off

    pp.ip_ver = 4
    pp.ttl = data[off + 8]
    pp.proto = data[off + 9]
    pp.src = socket.inet_ntop(socket.AF_INET, data[off + 12:off + 16])
    pp.dst = socket.inet_ntop(socket.AF_INET, data[off + 16:off + 20])
    pp.ip_len = total_len

    # Fragment offset is in the low 13 bits of the Flags+Fragment field.
    # If non-zero, this is a subsequent fragment and has no L4 header.
    flags_frag = u16be(data, off + 6)
    frag_offset = flags_frag & 0x1FFF

    transport_off = off + ihl
    end = off + total_len

    if frag_offset == 0:
        parse_transport(pp.proto, data, transport_off, pp, end)


# ===========================================================================
# IPv6 parser (RFC 8200).
# Walks the extension header chain (Hop-by-Hop, Routing, Fragment, AH, etc.)
# to find the upper-layer protocol.  Only the first fragment is parsed
# for transport data.  Extension header loop detection via a seen-set.
# ===========================================================================
def parse_ipv6(data, off, pp):
    if len(data) < off + 40:
        return

    pp.ip_ver = 6
    payload_len = u16be(data, off + 4)   # Length of everything after the 40-byte header.
    next_header = data[off + 6]          # First Next Header value.
    pp.ttl = data[off + 7]               # Hop Limit (analogous to IPv4 TTL).
    pp.src = socket.inet_ntop(socket.AF_INET6, data[off + 8:off + 24])
    pp.dst = socket.inet_ntop(socket.AF_INET6, data[off + 24:off + 40])
    pp.ip_len = 40 + payload_len

    end = off + 40 + payload_len
    if end > len(data):
        end = len(data)

    nh = next_header
    off2 = off + 40       # Current parse position (start of first extension header).
    frag_offset = 0
    upper = None           # Will hold the final upper-layer protocol number.
    seen = set()           # Loop detection for malformed extension chains.

    while off2 < end:
        # If we've reached a transport protocol, stop walking.
        if nh in (6, 17, 58):  # TCP, UDP, ICMPv6
            upper = nh
            break
        if nh == 59:  # No Next Header: explicit end.
            break
        if off2 in seen:  # Circular extension header chain.
            break
        seen.add(off2)

        if nh in (0, 43, 60, 135, 139, 140):
            # Hop-by-Hop(0), Routing(43), Destination(60), Mobility(135),
            # HIP(139), Shim6(140): all share the TLV extension header format.
            # Length field is in 8-octet units, excluding the first 8 octets.
            if end < off2 + 2:
                break
            ext_len = (data[off2 + 1] + 1) * 8
            if end < off2 + ext_len:
                break
            nh = data[off2]  # Next Header field is the first byte.
            off2 += ext_len

        elif nh == 44:
            # Fragment header (RFC 8200 Section 4.5): fixed 8 bytes.
            if end < off2 + 8:
                break
            nh = data[off2]
            # Fragment offset is bits 3-15 of byte 2; low 3 bits are flags.
            frag_offset = (data[off2 + 2] & 0xF8) >> 3
            off2 += 8
            if frag_offset != 0:
                # Non-first fragment: no transport header present.
                break

        elif nh == 51:
            # Authentication Header (RFC 4302): variable length.
            if end < off2 + 2:
                break
            ext_len = (data[off2 + 1] + 2) * 4
            if end < off2 + ext_len:
                break
            nh = data[off2]
            off2 += ext_len

        else:
            # Unknown extension header type: stop parsing.
            break

    pp.proto = nh
    if upper is not None and frag_offset == 0:
        parse_transport(upper, data, off2, pp, end)


# ===========================================================================
# Top-level packet parser.
# Dispatches on link-layer type to strip the L2 header, determine the
# EtherType (or IP version for RAW), and hand off to the IP parser.
# Returns a ParsedPacket with all decoded fields populated.
# ===========================================================================
def parse_packet(linktype, data):
    pp = ParsedPacket()
    if not data:
        return pp

    offset = 0
    ethertype = None

    if linktype == 1:
        # --- Ethernet II (IEEE 802.3) ---
        # 14-byte header: DstMAC(6) SrcMAC(6) EtherType(2).
        if len(data) < 14:
            return pp
        pp.eth_dst = ":".join(f"{b:02x}" for b in data[0:6])
        pp.eth_src = ":".join(f"{b:02x}" for b in data[6:12])
        ethertype = u16be(data, 12)
        offset = 14

        # Handle 802.1Q (0x8100) and 802.1ad (0x88A8) VLAN tags.
        # There can be multiple stacked tags (Q-in-Q).
        while ethertype in (0x8100, 0x88A8) and len(data) >= offset + 4:
            vlan_tci = u16be(data, offset)
            pp.vlan = vlan_tci & 0x0FFF  # VLAN ID is the low 12 bits.
            ethertype = u16be(data, offset + 2)
            offset += 4

    elif linktype == 101:
        # --- Raw IP (DLT_RAW) ---
        # No L2 header.  The first nibble indicates the IP version.
        version = data[0] >> 4
        if version == 4:
            ethertype = 0x0800
        elif version == 6:
            ethertype = 0x86DD
        else:
            return pp
        offset = 0

    elif linktype == 113:
        # --- Linux SLL ("cooked" capture, DLT_LINUX_SLL) ---
        # 16-byte pseudo-header: pkttype(2) arphrd(2) addr_len(2) addr(8) proto(2).
        if len(data) < 16:
            return pp
        ethertype = u16be(data, 14)
        offset = 16

    elif linktype == 0:
        # --- BSD Null/Loopback (DLT_NULL) ---
        # 4-byte header containing the address family in host byte order.
        # AF_INET = 2, AF_INET6 = 10/24/28/30 depending on BSD variant.
        if len(data) < 4:
            return pp
        family_le = struct.unpack_from("<I", data, 0)[0]
        family_be = struct.unpack_from(">I", data, 0)[0]
        if family_le == 2 or family_be == 2:
            ethertype = 0x0800
        elif family_le in (10, 24, 28, 30) or family_be in (10, 24, 28, 30):
            ethertype = 0x86DD
        offset = 4

    else:
        # Unsupported link type: return empty ParsedPacket.
        return pp

    # Dispatch to the appropriate network-layer parser.
    if ethertype == 0x0800:
        parse_ipv4(data, offset, pp)
    elif ethertype == 0x86DD:
        parse_ipv6(data, offset, pp)
    elif ethertype == 0x0806:
        # ARP: no IP header.  Label it for protocol statistics.
        pp.app = "ARP"

    return pp


# ===========================================================================
# File input handling.
# Transparently opens gzip-compressed captures (magic bytes 0x1f 0x8b).
# ===========================================================================
def open_input(path):
    with open(path, "rb") as f:
        magic = f.read(2)
    if magic == b"\x1f\x8b":
        return gzip.open(path, "rb")
    return open(path, "rb")


# ===========================================================================
# pcapng option parser (TLV format).
# Options appear in Interface Description Blocks (IDB) and other blocks.
# Each option: Code(2) Length(2) Value(Length) Padding(to 32-bit boundary).
# Code 0 = opt_endofopt (terminator).
# ===========================================================================
def parse_options(data, endian):
    opts = {}
    off = 0
    while off + 4 <= len(data):
        code, length = struct.unpack_from(endian + "HH", data, off)
        off += 4
        if code == 0:  # End-of-options sentinel.
            break
        if off + length > len(data):
            break
        opts[code] = data[off:off + length]
        off += length
        # Pad to next 32-bit boundary (pcapng spec requirement).
        off += (4 - (length % 4)) % 4
    return opts


def tsresol_to_scale(value_byte):
    """
    Convert the if_tsresol option byte to a seconds-per-tick multiplier.
    If the high bit is set, the resolution is 2^-(low 7 bits) seconds.
    Otherwise, it is 10^-(value) seconds.
    Reference: pcapng spec, Section 4.2, if_tsresol.
    """
    if value_byte & 0x80:
        return 2.0 ** (-(value_byte & 0x7F))
    return 10.0 ** (-value_byte)


# ===========================================================================
# Classic pcap reader (libpcap format).
# Global header (24 bytes) -> per-packet record headers (16 bytes each).
# Supports both microsecond (magic 0xA1B2C3D4) and nanosecond (0xA1B23C4D)
# timestamp resolutions, and both little-endian and big-endian byte orders.
# Yields: (timestamp_seconds, captured_length, original_length, raw_bytes, linktype).
# ===========================================================================
def pcap_classic_packets(fh, first4):
    try:
        rest = fh.read(20)
        header = first4 + rest
        if len(header) < 24:
            raise ValueError("Truncated pcap global header")

        # Determine byte order and timestamp resolution from the magic number.
        magic_le = struct.unpack("<I", header[:4])[0]
        if magic_le in (0xA1B2C3D4, 0xA1B23C4D):
            endian = "<"
            nano = magic_le == 0xA1B23C4D
        else:
            magic_be = struct.unpack(">I", header[:4])[0]
            if magic_be in (0xA1B2C3D4, 0xA1B23C4D):
                endian = ">"
                nano = magic_be == 0xA1B23C4D
            else:
                raise ValueError("Unsupported pcap magic")

        # Global header fields: major(2) minor(2) thiszone(4) sigfigs(4) snaplen(4) network(4).
        _major, _minor, _thiszone, _sigfigs, _snaplen, network = struct.unpack(
            endian + "HHiIII", header[4:24]
        )

        # Convert the fractional timestamp part to seconds.
        ts_scale = 1e-9 if nano else 1e-6

        while True:
            # Per-packet record header: ts_sec(4) ts_frac(4) incl_len(4) orig_len(4).
            rec = fh.read(16)
            if len(rec) < 16:
                break  # EOF or truncated file.

            ts_sec, ts_frac, incl_len, orig_len = struct.unpack(endian + "IIII", rec)
            # Guard against corrupt files claiming absurd packet sizes.
            if incl_len > 100_000_000:
                raise ValueError(f"Packet length too large: {incl_len}")

            data = fh.read(incl_len)
            if len(data) < incl_len:
                break  # Truncated packet at end of file.

            ts = ts_sec + ts_frac * ts_scale
            yield ts, incl_len, orig_len, data, network

    finally:
        fh.close()


# ===========================================================================
# pcapng reader (PCAP Next Generation, IETF draft-tuexen-opsawg-pcapng).
# Block-based format: Section Header Block (SHB) -> Interface Description
# Blocks (IDB) -> Enhanced Packet Blocks (EPB) / Simple Packet Blocks (SPB).
# Supports mid-file endianness changes (new SHB) and multiple interfaces.
# Yields: (timestamp_seconds, captured_length, original_length, raw_bytes, linktype).
# ===========================================================================
def pcapng_packets(fh, first4):
    try:
        # The first 4 bytes (0x0A0D0D0A) were already consumed by iter_packets().
        # Read the rest of the SHB: Block Total Length(4) + Byte-Order Magic(4).
        extra = fh.read(8)
        if len(extra) < 8:
            raise ValueError("Truncated pcapng section header block")

        len_raw = extra[:4]
        magic_raw = extra[4:8]

        # Byte-Order Magic determines endianness for this section.
        if magic_raw == b"\x4d\x3c\x2b\x1a":
            endian = "<"
        elif magic_raw == b"\x1a\x2b\x3c\x4d":
            endian = ">"
        else:
            raise ValueError("Unsupported pcapng byte order")

        block_len = struct.unpack(endian + "I", len_raw)[0]
        if block_len < 12:
            raise ValueError("Invalid pcapng SHB length")
        if block_len > 100_000_000:
            raise ValueError(f"Pcapng block length too large: {block_len}")

        # Skip the remainder of the SHB (options, trailing length, etc.).
        remaining = block_len - 12
        _ = fh.read(remaining)

        # Track interface parameters (linktype, timestamp scale) by interface ID.
        interfaces = {}

        while True:
            # Every block starts with: Block Type(4) Block Total Length(4).
            hdr = fh.read(8)
            if len(hdr) < 8:
                break  # EOF.

            block_type, block_len = struct.unpack(endian + "II", hdr)
            if block_len < 12:
                raise ValueError("Invalid pcapng block length")
            if block_len > 100_000_000:
                raise ValueError(f"Pcapng block length too large: {block_len}")

            # Read the block body + trailing Block Total Length (4 bytes).
            body_with_trailer = fh.read(block_len - 8)
            if len(body_with_trailer) < block_len - 8:
                break  # Truncated block.

            # Strip the trailing 4-byte Block Total Length copy.
            body = body_with_trailer[:-4]

            if block_type == 0x0A0D0D0A:
                # --- Section Header Block (SHB) ---
                # A new SHB can appear mid-file with a different endianness.
                # Reset interface state since IDs are section-scoped.
                if len(body) >= 4:
                    if body[:4] == b"\x4d\x3c\x2b\x1a":
                        endian = "<"
                    elif body[:4] == b"\x1a\x2b\x3c\x4d":
                        endian = ">"
                interfaces.clear()

            elif block_type == 0x00000001:
                # --- Interface Description Block (IDB) ---
                # Defines link type, snap length, and timestamp resolution
                # for packets captured on this interface.
                if len(body) >= 8:
                    linktype = struct.unpack(endian + "H", body[0:2])[0]
                    snaplen = struct.unpack(endian + "I", body[4:8])[0]
                    opts = parse_options(body[8:], endian)

                    # Default timestamp resolution is microseconds (10^-6).
                    scale = 1e-6
                    if 9 in opts and opts[9]:
                        # Option 9 = if_tsresol.
                        scale = tsresol_to_scale(opts[9][0])

                    interfaces[len(interfaces)] = {
                        "linktype": linktype,
                        "snaplen": snaplen,
                        "scale": scale,
                    }

            elif block_type == 0x00000006:
                # --- Enhanced Packet Block (EPB) ---
                # The primary packet container in pcapng.
                # Layout: InterfaceID(4) TimestampHigh(4) TimestampLow(4)
                #         CapturedLen(4) OriginalLen(4) PacketData(...) Options(...)
                if len(body) >= 20:
                    iface_id, ts_high, ts_low, caplen, origlen = struct.unpack(
                        endian + "IIIII", body[:20]
                    )
                    # Clamp caplen to available data (defensive against corruption).
                    max_cap = max(0, len(body) - 20)
                    if caplen > max_cap:
                        caplen = max_cap

                    data = body[20:20 + caplen]
                    iface = interfaces.get(iface_id, {"linktype": 1, "scale": 1e-6})
                    # Reconstruct the 64-bit timestamp and convert to seconds.
                    ts_raw = (ts_high << 32) | ts_low
                    ts = ts_raw * iface.get("scale", 1e-6)

                    yield ts, caplen, origlen, data, iface.get("linktype", 1)

            elif block_type == 0x00000003:
                # --- Simple Packet Block (SPB) ---
                # Minimal packet container: OriginalLen(4) + PacketData(...).
                # No timestamp; always associated with interface 0.
                if len(body) >= 4:
                    packet_len = struct.unpack(endian + "I", body[:4])[0]
                    data = body[4:4 + packet_len]
                    iface = interfaces.get(0, {"linktype": 1, "scale": 1e-6})
                    yield 0.0, len(data), packet_len, data, iface.get("linktype", 1)

    finally:
        fh.close()


# ===========================================================================
# Format detection and packet iteration entry point.
# Reads the first 4 bytes to distinguish pcapng (0x0A0D0D0A) from classic
# pcap (0xA1B2C3D4 / 0xA1B23C4D in either byte order).
# Returns (format_string, generator_of_packets).
# ===========================================================================
def iter_packets(path):
    fh = open_input(path)
    first4 = fh.read(4)

    if len(first4) < 4:
        fh.close()
        return "empty", iter([])

    # pcapng Section Header Block starts with 0x0A0D0D0A (palindromic, so
    # byte order is determined later from the Byte-Order Magic field).
    if first4 == b"\x0a\x0d\x0d\x0a":
        return "pcapng", pcapng_packets(fh, first4)

    # Otherwise assume classic pcap (byte order determined inside the reader).
    return "pcap", pcap_classic_packets(fh, first4)


# ===========================================================================
# Analyzer: the central accumulation engine.
# Receives parsed packets one at a time, dispatches to protocol-specific
# handlers, and accumulates statistics and event lists.  The report()
# method serializes all accumulated state into a plain dict suitable for
# JSON output or table rendering.
# ===========================================================================
class Analyzer:
    def __init__(self, features, limit=20, reveal=False):
        self.features = set(features)
        self.limit = max(1, int(limit))  # Max stored events per section.
        self.reveal = reveal             # If False, secrets are redacted.

        self.path = ""
        self.file_type = "unknown"
        self.linktypes = set()

        # --- Summary counters ---
        self.packet_count = 0
        self.bytes_cap = 0       # Sum of captured lengths.
        self.bytes_orig = 0      # Sum of original (on-wire) lengths.
        self.first_ts = None     # Earliest packet timestamp.
        self.last_ts = None      # Latest packet timestamp.

        # --- Protocol distribution counters ---
        self.ip_versions = Counter()   # {"IPv4": N, "IPv6": M}
        self.ip_protocols = Counter()  # {"TCP": N, "UDP": M, ...}
        self.ports = Counter()         # {"tcp/443": N, "udp/53": M, ...}
        self.apps = Counter()          # {"HTTP": N, "DNS": M, ...}
        self.tcp_flags = Counter()     # {"SYN": N, "ACK": M, ...}

        # --- Conversation tracking: (ip_a, ip_b, proto) -> {packets, bytes} ---
        self.conv = defaultdict(lambda: {"packets": 0, "bytes": 0})

        # --- DNS analysis state ---
        self.dns = {
            "query_count": 0,
            "response_count": 0,
            "suspicious_count": 0,
            "queries": [],       # Bounded list of query events.
            "responses": [],     # Bounded list of response events.
            "suspicious": [],    # Bounded list of suspicious query events.
        }

        # --- HTTP analysis state ---
        self.http = {
            "request_count": 0,
            "response_count": 0,
            "events": [],        # Bounded list of request/response events.
        }

        # --- TLS analysis state ---
        self.tls = {
            "count": 0,
            "events": [],        # Bounded list of ClientHello events.
        }

        # --- Credential exposure state ---
        self.creds = {
            "count": 0,
            "events": [],        # Bounded list of credential events.
        }

        # --- Anomaly detection state ---
        self.anomalies = {
            "counts": Counter(), # Anomaly type -> occurrence count.
            "events": [],        # Bounded list of individual anomaly events.
        }

        # Pre-compute which protocol parsers are needed based on selected features.
        # This avoids unnecessary parsing overhead when a feature is disabled.
        self.parse_dns = bool(self.features & {"dns", "anomalies"})
        self.parse_http = bool(self.features & {"http", "creds", "anomalies"})
        self.parse_tls = "tls" in self.features
        self.parse_ftp = "creds" in self.features
        self.detect_anomalies_flag = "anomalies" in self.features

    def add_event(self, bucket, event):
        """Append an event to a bounded list. Silently drops events beyond the limit."""
        if len(bucket) < self.limit:
            bucket.append(event)

    def redact(self, value):
        """Replace a secret value with asterisks unless --reveal-secrets is set."""
        if value is None:
            return ""
        value = str(value)
        if self.reveal:
            return value
        return "********"

    def add_cred(self, protocol, cred_type, src, dst, detail, ts):
        """Record a credential exposure event."""
        self.creds["count"] += 1
        event = {
            "time": ts_to_str(ts),
            "protocol": protocol,
            "type": cred_type,
            "src": src,
            "dst": dst,
            "detail": detail,
        }
        self.add_event(self.creds["events"], event)

    def add_anomaly(self, atype, src, dst, detail, ts):
        """Record a network anomaly event and increment its type counter."""
        self.anomalies["counts"][atype] += 1
        event = {
            "time": ts_to_str(ts),
            "type": atype,
            "src": src,
            "dst": dst,
            "detail": detail,
        }
        self.add_event(self.anomalies["events"], event)

    def suspicious_dns(self, name):
        """
        Heuristic DNS name analysis for DGA / tunneling detection.
        Returns a list of human-readable reason strings (empty = not suspicious).
        Thresholds are intentionally conservative to reduce false positives.
        """
        reasons = []
        if len(name) > 60:
            reasons.append("long name")
        if name.count(".") > 6:
            reasons.append("many labels")
        longest_label = max((len(label) for label in name.split(".")), default=0)
        if longest_label > 32:
            reasons.append("long label")
        # High entropy in a sufficiently long name suggests random generation.
        if len(name) > 20 and shannon_entropy(name) > 3.8:
            reasons.append("high entropy")
        return reasons

    def handle_dns(self, pp, ts):
        """Parse a DNS payload and record queries, responses, and suspicious names."""
        parsed = parse_dns(pp.payload, pp.proto == 6)
        if not parsed:
            return

        pp.app = "DNS"
        self.apps["DNS"] += 1

        if parsed["qr"] == 0:
            # --- DNS Query ---
            self.dns["query_count"] += max(1, len(parsed["questions"]))
            for q in parsed["questions"]:
                event = {
                    "time": ts_to_str(ts),
                    "client": pp.src,
                    "server": pp.dst,
                    "query": q["name"],
                    "type": q["type"],
                }
                self.add_event(self.dns["queries"], event)

                # Run suspicious-name heuristics on every queried domain.
                reasons = self.suspicious_dns(q["name"])
                if reasons:
                    self.dns["suspicious_count"] += 1
                    susp_event = {
                        "time": ts_to_str(ts),
                        "client": pp.src,
                        "server": pp.dst,
                        "query": q["name"],
                        "reason": ", ".join(reasons),
                    }
                    self.add_event(self.dns["suspicious"], susp_event)
                    self.add_anomaly(
                        "DNS suspicious query",
                        pp.src,
                        pp.dst,
                        f"{q['name']} ({', '.join(reasons)})",
                        ts,
                    )
        else:
            # --- DNS Response ---
            self.dns["response_count"] += 1
            # Extract the first question and first answer for summary display.
            name = parsed["questions"][0]["name"] if parsed["questions"] else ""
            rtype = parsed["answers"][0]["type"] if parsed["answers"] else ""
            data = parsed["answers"][0]["data"] if parsed["answers"] else ""
            if parsed["rcode"] != 0:
                # Non-zero rcode (e.g. NXDOMAIN) is prepended for visibility.
                data = f"rcode={parsed['rcode']} {data}".strip()

            event = {
                "time": ts_to_str(ts),
                "server": pp.src,
                "client": pp.dst,
                "name": name,
                "type": rtype,
                "data": data,
            }
            self.add_event(self.dns["responses"], event)

    def extract_http_creds(self, event, pp, ts):
        """
        Scan an HTTP event for credential material:
        - Authorization header (Basic, Bearer, etc.)
        - Cookie / Set-Cookie headers (names only, values redacted)
        - URL-encoded form fields whose names match secret patterns
        """
        headers = event.get("headers", {})

        # --- Authorization header ---
        auth = headers.get("authorization")
        if auth:
            if auth.lower().startswith("basic "):
                # Basic auth: base64("username:password").
                try:
                    decoded = base64.b64decode(auth[6:].strip()).decode("utf-8", "replace")
                    user, _, secret = decoded.partition(":")
                    detail = f"user={user or 'N/A'} password={self.redact(secret)}"
                except Exception:
                    detail = f"Authorization: Basic {self.redact(auth[6:].strip())}"
                self.add_cred("HTTP", "Basic Auth", pp.src, pp.dst, detail, ts)
            else:
                # Bearer, Digest, or other schemes: log the scheme, redact the token.
                scheme = auth.split(" ", 1)[0]
                self.add_cred("HTTP", f"{scheme} Authorization", pp.src, pp.dst,
                              f"Authorization: {self.redact(auth)}", ts)

        # --- Cookie header (client -> server) ---
        cookie = headers.get("cookie")
        if cookie:
            names = cookie_names(cookie)
            self.add_cred(
                "HTTP",
                "Cookie",
                pp.src,
                pp.dst,
                f"Cookie names: {', '.join(names) if names else 'unknown'}",
                ts,
            )

        # --- Set-Cookie header (server -> client) ---
        set_cookie = headers.get("set-cookie")
        if set_cookie:
            names = cookie_names(set_cookie)
            self.add_cred(
                "HTTP",
                "Set-Cookie",
                pp.src,
                pp.dst,
                f"Set-Cookie names: {', '.join(names) if names else 'unknown'}",
                ts,
            )

        # --- Form fields with secret-sounding names ---
        for field in event.get("form_fields", []):
            name = field.get("name", "")
            if is_secret_field(name):
                self.add_cred(
                    "HTTP",
                    "Form Secret",
                    pp.src,
                    pp.dst,
                    f"field={name} value={self.redact(field.get('value', ''))}",
                    ts,
                )

    def handle_http(self, pp, ts):
        """Parse an HTTP payload, record the event, extract creds, detect URI anomalies."""
        event = parse_http(pp.payload)
        if not event:
            return

        pp.app = "HTTP"
        self.apps["HTTP"] += 1

        event["time"] = ts_to_str(ts)
        event["src"] = pp.src
        event["dst"] = pp.dst
        event["sport"] = pp.sport
        event["dport"] = pp.dport

        if event["kind"] == "request":
            self.http["request_count"] += 1
            event["detail"] = f"{event.get('method', '')} {event.get('url', '')}".strip()
        else:
            self.http["response_count"] += 1
            event["detail"] = f"{event.get('status', '')} {event.get('reason', '')}".strip()

        self.add_event(self.http["events"], event)

        # Credential extraction (only if the "creds" feature is enabled).
        if "creds" in self.features:
            self.extract_http_creds(event, pp, ts)

        # URI-based anomaly detection: look for common attack patterns.
        if self.detect_anomalies_flag and event["kind"] == "request":
            uri = event.get("uri", "").lower()
            patterns = (
                "../",              # Path traversal
                "/etc/passwd",      # Path traversal target
                "cmd=",             # Command injection parameter
                "exec=",            # Command injection parameter
                "shell",            # Web shell access
                "union+select",     # SQL injection (space-encoded)
                "union%20select",   # SQL injection (URL-encoded)
                "base64_decode",    # PHP code injection
            )
            hits = [pat for pat in patterns if pat in uri]
            if hits:
                self.add_anomaly(
                    "HTTP suspicious URI",
                    pp.src,
                    pp.dst,
                    f"{event.get('method', '')} {event.get('uri', '')} ({', '.join(hits)})",
                    ts,
                )

    def handle_tls(self, pp, ts):
        """Parse a TLS ClientHello and record SNI / version metadata."""
        parsed = parse_tls(pp.payload)
        if not parsed:
            return

        pp.app = "TLS"
        self.apps["TLS"] += 1
        self.tls["count"] += 1

        event = {
            "time": ts_to_str(ts),
            "src": pp.src,
            "dst": pp.dst,
            "sni": parsed.get("sni") or "N/A",
            "version": parsed.get("version", ""),
            "ciphers": parsed.get("cipher_suites", 0),
        }
        self.add_event(self.tls["events"], event)

    def handle_ftp(self, pp, ts):
        """Parse FTP control channel for USER/PASS commands (cleartext creds)."""
        parsed = parse_ftp(pp.payload)
        if not parsed:
            return

        pp.app = "FTP"
        self.apps["FTP"] += 1

        if parsed["kind"] == "command":
            if parsed["command"] == "USER":
                self.add_cred("FTP", "FTP USER", pp.src, pp.dst,
                              f"user={parsed['value']}", ts)
            elif parsed["command"] == "PASS":
                # Password is redacted unless --reveal-secrets is active.
                self.add_cred("FTP", "FTP PASS", pp.src, pp.dst,
                              f"password={self.redact(parsed['value'])}", ts)

    def detect_anomalies(self, pp, ts):
        """
        Per-packet anomaly detection.  Checks for:
        - TCP NULL scan (all flags cleared)
        - TCP XMAS scan (FIN+URG+PSH)
        - TCP SYN-FIN (invalid combination)
        - TCP FIN-only (FIN without ACK, SYN, or RST)
        - TCP RST count (informational)
        - TCP SYN-without-ACK count (informational, normal during connection setup)
        - Oversized ICMP payloads (possible tunnel or ping-of-death)
        """
        if pp.proto == 6 and pp.tcp_flags is not None:
            f = pp.tcp_flags

            # NULL scan: no flags set at all.  Nmap -sN signature.
            if f == 0:
                self.add_anomaly("TCP NULL scan", pp.src, pp.dst, "TCP flags=0x00", ts)

            # XMAS scan: FIN + URG + PSH.  Nmap -sX signature.
            if (f & 0x01) and (f & 0x20) and (f & 0x08):
                self.add_anomaly("TCP XMAS scan", pp.src, pp.dst, "FIN+URG+PSH", ts)

            # SYN+FIN is an invalid combination per RFC 9293.
            # Some OS fingerprinting tools and stealth scanners use this.
            if (f & 0x02) and (f & 0x01):
                self.add_anomaly("TCP SYN-FIN", pp.src, pp.dst, "SYN and FIN set", ts)

            # FIN without ACK, SYN, or RST: FIN scan (Nmap -sF).
            if (f & 0x01) and not (f & 0x10) and not (f & 0x02) and not (f & 0x04):
                self.add_anomaly("TCP FIN only", pp.src, pp.dst,
                                 "FIN without ACK/SYN/RST", ts)

            # Informational counters (not flagged as anomalies, just tallied).
            if f & 0x04:
                self.anomalies["counts"]["TCP RST"] += 1

            if (f & 0x02) and not (f & 0x10):
                self.anomalies["counts"]["TCP SYN without ACK"] += 1

        # Large ICMP payloads may indicate ICMP tunneling or ping-of-death.
        if pp.proto in (1, 58) and pp.icmp_type is not None:
            if len(pp.payload) > 1000:
                self.add_anomaly(
                    "Large ICMP payload",
                    pp.src,
                    pp.dst,
                    f"payload_bytes={len(pp.payload)}",
                    ts,
                )

    def process_packet(self, ts, caplen, origlen, data, linktype):
        """
        Main per-packet entry point called by the iteration loop.
        Decodes the packet, updates all counters, and dispatches to
        protocol-specific handlers based on enabled features.
        """
        self.packet_count += 1
        self.bytes_cap += caplen
        self.bytes_orig += origlen

        # Track the time span of the capture.
        if self.first_ts is None or ts < self.first_ts:
            self.first_ts = ts
        if self.last_ts is None or ts > self.last_ts:
            self.last_ts = ts

        self.linktypes.add(linktype)

        # Decode L2/L3/L4 into a ParsedPacket.
        pp = parse_packet(linktype, data)

        # --- Update protocol distribution counters ---
        if pp.ip_ver:
            self.ip_versions[f"IPv{pp.ip_ver}"] += 1

        if pp.proto is not None:
            name = IP_PROTOS.get(pp.proto, f"IPProto-{pp.proto}")
            self.ip_protocols[name] += 1

        if pp.dport is not None and pp.proto is not None:
            if pp.proto == 6:
                port_label = f"tcp/{pp.dport}"
            elif pp.proto == 17:
                port_label = f"udp/{pp.dport}"
            else:
                port_label = f"ipproto-{pp.proto}/{pp.dport}"
            self.ports[port_label] += 1

        if pp.app:
            self.apps[pp.app] += 1

        # --- Update conversation table ---
        # Conversations are keyed by sorted (ip_a, ip_b, proto) so that
        # A->B and B->A are merged into a single entry.
        if pp.src and pp.dst:
            proto_label = IP_PROTOS.get(pp.proto, "Other") if pp.proto is not None else "Other"
            a, b = sorted((pp.src, pp.dst))
            key = (a, b, proto_label)
            self.conv[key]["packets"] += 1
            self.conv[key]["bytes"] += origlen

        # --- Update TCP flag counters ---
        if pp.tcp_flags is not None:
            for name, mask in TCP_FLAG_NAMES.items():
                if pp.tcp_flags & mask:
                    self.tcp_flags[name] += 1

        # --- Application-layer protocol dispatch ---
        # Only attempt L7 parsing when there is a transport payload and
        # the relevant feature is enabled.
        if pp.proto in (6, 17) and pp.payload:
            ports = (pp.sport, pp.dport)

            # DNS: port 53 on either TCP or UDP.
            if self.parse_dns and 53 in ports:
                self.handle_dns(pp, ts)

            if pp.proto == 6:
                # HTTP: heuristic detection on TCP payloads.
                if self.parse_http and looks_http(pp.payload, pp.sport, pp.dport):
                    self.handle_http(pp, ts)

                # TLS: check for Handshake content type (0x16).
                if self.parse_tls and is_tls(pp.payload):
                    self.handle_tls(pp, ts)

                # FTP: control channel on port 21.
                if self.parse_ftp and 21 in ports:
                    self.handle_ftp(pp, ts)

        # --- Anomaly detection (runs on every packet if enabled) ---
        if self.detect_anomalies_flag:
            self.detect_anomalies(pp, ts)

    def report(self):
        """
        Serialize all accumulated analysis state into a plain dict.
        This dict is suitable for JSON serialization or table rendering.
        Sections corresponding to disabled features are set to None.
        """
        duration = 0.0
        if self.first_ts is not None and self.last_ts is not None and self.last_ts > self.first_ts:
            duration = self.last_ts - self.first_ts

        # Average packets per second (guard against zero-duration captures).
        pps = self.packet_count / duration if duration > 0 else float(self.packet_count)

        return {
            "file": self.path,
            "file_type": self.file_type,
            "features": sorted(self.features),
            "summary": {
                "packet_count": self.packet_count,
                "captured_bytes": self.bytes_cap,
                "original_bytes": self.bytes_orig,
                "first_ts": ts_to_str(self.first_ts),
                "last_ts": ts_to_str(self.last_ts),
                "duration_seconds": round(duration, 6),
                "avg_packets_per_second": round(pps, 3),
                "linktypes": sorted({LINKTYPES.get(x, str(x)) for x in self.linktypes}),
            },
            "protocols": {
                "ip_versions": dict(self.ip_versions),
                "ip_protocols": dict(self.ip_protocols),
                "destination_ports": dict(self.ports.most_common(self.limit)),
                "applications": dict(self.apps),
                "tcp_flags": dict(self.tcp_flags),
            },
            "conversations": [
                {
                    "endpoint_a": k[0],
                    "endpoint_b": k[1],
                    "protocol": k[2],
                    "packets": v["packets"],
                    "bytes": v["bytes"],
                }
                # Sort by byte volume descending; take top N.
                for k, v in sorted(self.conv.items(), key=lambda kv: kv[1]["bytes"], reverse=True)[:self.limit]
            ],
            "dns": self.dns if "dns" in self.features else None,
            "http": self.http if "http" in self.features else None,
            "tls": self.tls if "tls" in self.features else None,
            "creds": self.creds if "creds" in self.features else None,
            "anomalies": {
                "counts": dict(self.anomalies["counts"]),
                "events": self.anomalies["events"],
            } if "anomalies" in self.features else None,
        }


# ===========================================================================
# Report renderer: converts the Analyzer.report() dict into formatted
# ASCII tables printed to stdout.  Each section is only rendered if the
# corresponding feature was enabled.
# ===========================================================================
def print_report(analyzer, painter):
    rep = analyzer.report()
    print_banner(painter, "PCAP ANALYSIS REPORT")

    # --- Summary section ---
    if "summary" in analyzer.features:
        s = rep["summary"]
        rows = [
            ("File", rep["file"]),
            ("File type", rep["file_type"]),
            ("Link types", ", ".join(s["linktypes"]) or "N/A"),
            ("Packets", s["packet_count"]),
            ("Captured bytes", f"{s['captured_bytes']} ({human_bytes(s['captured_bytes'])})"),
            ("Original bytes", f"{s['original_bytes']} ({human_bytes(s['original_bytes'])})"),
            ("First packet", s["first_ts"]),
            ("Last packet", s["last_ts"]),
            ("Duration", f"{s['duration_seconds']} s"),
            ("Average pps", s["avg_packets_per_second"]),
        ]
        print_section(painter, "Summary", render_table(painter, ["Metric", "Value"], rows))

    # --- Protocol hierarchy section ---
    if "protocols" in analyzer.features:
        proto = rep["protocols"]

        rows = [(k, v) for k, v in sorted(proto["ip_versions"].items(), key=lambda x: x[1], reverse=True)]
        print_section(painter, "Protocol Hierarchy", render_table(painter, ["IP Version", "Packets"], rows))

        rows = [(k, v) for k, v in sorted(proto["ip_protocols"].items(), key=lambda x: x[1], reverse=True)]
        print_section(painter, "IP Protocols", render_table(painter, ["Protocol", "Packets"], rows))

        rows = [(k, v) for k, v in sorted(proto["destination_ports"].items(), key=lambda x: x[1], reverse=True)]
        print_section(painter, "Top Destination Ports", render_table(painter, ["Port", "Packets"], rows))

        rows = [(k, v) for k, v in sorted(proto["applications"].items(), key=lambda x: x[1], reverse=True)]
        print_section(painter, "Application Protocols", render_table(painter, ["Application", "Packets"], rows))

        rows = [(k, v) for k, v in sorted(proto["tcp_flags"].items(), key=lambda x: x[1], reverse=True)]
        print_section(painter, "TCP Flags", render_table(painter, ["Flag", "Packets"], rows))

    # --- Conversations section ---
    if "conversations" in analyzer.features:
        rows = [
            (
                c["endpoint_a"],
                c["endpoint_b"],
                c["protocol"],
                c["packets"],
                f"{c['bytes']} ({human_bytes(c['bytes'])})",
            )
            for c in rep["conversations"]
        ]
        print_section(painter, "Top Conversations",
                      render_table(painter, ["Endpoint A", "Endpoint B", "Protocol", "Packets", "Bytes"], rows))

    # --- DNS section ---
    if "dns" in analyzer.features and rep["dns"]:
        d = rep["dns"]
        rows = [
            ("Queries", d["query_count"]),
            ("Responses", d["response_count"]),
            ("Suspicious queries", d["suspicious_count"]),
            ("Stored query events", len(d["queries"])),
            ("Stored response events", len(d["responses"])),
        ]
        print_section(painter, "DNS Summary", render_table(painter, ["Metric", "Value"], rows))

        rows = [(q["time"], q["client"], q["server"], q["query"], q["type"]) for q in d["queries"]]
        print_section(painter, "DNS Queries",
                      render_table(painter, ["Time", "Client", "Server", "Query", "Type"], rows))

        rows = [(r["time"], r["server"], r["client"], r["name"], r["type"], r["data"]) for r in d["responses"]]
        print_section(painter, "DNS Responses",
                      render_table(painter, ["Time", "Server", "Client", "Name", "Type", "Data"], rows))

        # Suspicious queries are highlighted in yellow.
        if d["suspicious"]:
            rows = [(s["time"], s["client"], s["server"], s["query"], s["reason"]) for s in d["suspicious"]]
            colors = ["yellow"] * len(rows)
            print_section(painter, "Suspicious DNS",
                          render_table(painter, ["Time", "Client", "Server", "Query", "Reason"], rows, colors),
                          title_color="yellow")

    # --- HTTP section ---
    if "http" in analyzer.features and rep["http"]:
        h = rep["http"]
        rows = [
            ("Requests", h["request_count"]),
            ("Responses", h["response_count"]),
            ("Stored events", len(h["events"])),
        ]
        print_section(painter, "HTTP Summary", render_table(painter, ["Metric", "Value"], rows))

        rows = [(e["time"], e["src"], e["dst"], e["kind"], e.get("detail", "")) for e in h["events"]]
        print_section(painter, "HTTP Events",
                      render_table(painter, ["Time", "Source", "Destination", "Kind", "Detail"], rows))

    # --- TLS section ---
    if "tls" in analyzer.features and rep["tls"]:
        t = rep["tls"]
        rows = [(e["time"], e["src"], e["dst"], e["sni"], e["version"], e["ciphers"]) for e in t["events"]]
        print_section(
            painter,
            f"TLS ClientHello Events (count={t['count']})",
            render_table(painter, ["Time", "Source", "Destination", "SNI", "Version", "Cipher Suites"], rows),
        )

    # --- Credential exposure section (highlighted in yellow) ---
    if "creds" in analyzer.features and rep["creds"]:
        c = rep["creds"]
        rows = [(e["time"], e["src"], e["dst"], e["protocol"], e["type"], e["detail"]) for e in c["events"]]
        colors = ["yellow"] * len(rows)
        print_section(
            painter,
            f"Credential Exposure (count={c['count']})",
            render_table(painter, ["Time", "Source", "Destination", "Protocol", "Type", "Detail"], rows, colors),
            title_color="yellow",
        )

    # --- Anomalies section (highlighted in red) ---
    if "anomalies" in analyzer.features and rep["anomalies"]:
        a = rep["anomalies"]

        rows = [(k, v) for k, v in sorted(a["counts"].items(), key=lambda x: x[1], reverse=True)]
        colors = ["red"] * len(rows)
        print_section(painter, "Anomaly Counts",
                      render_table(painter, ["Anomaly", "Count"], rows, colors),
                      title_color="red")

        rows = [(e["time"], e["type"], e["src"], e["dst"], e["detail"]) for e in a["events"]]
        colors = ["red"] * len(rows)
        print_section(painter, "Anomaly Events",
                      render_table(painter, ["Time", "Type", "Source", "Destination", "Detail"], rows, colors),
                      title_color="red")


# ===========================================================================
# CLI feature-list parser.
# Validates a comma-separated string against the FEATURES whitelist.
# Raises ValueError on unknown feature names.
# ===========================================================================
def parse_feature_list(value):
    items = {x.strip().lower() for x in value.split(",") if x.strip()}
    unknown = items - set(FEATURES)
    if unknown:
        raise ValueError(
            f"Unknown features: {', '.join(sorted(unknown))}. Valid features: {', '.join(FEATURES)}"
        )
    return items


def interactive_select(painter):
    """Prompt the user interactively to enable/disable each feature."""
    selected = set()
    print(painter.paint("Select features to run (y/n, default y):", "bold"))
    for feat in FEATURES:
        try:
            ans = input(f"  Enable {feat}? [Y/n]: ").strip().lower()
        except EOFError:
            ans = ""  # Non-interactive stdin: default to enabled.
        if ans in ("n", "no"):
            continue
        selected.add(feat)
    return selected


# ===========================================================================
# Packet construction helpers for the self-test.
# These build minimal but valid Ethernet/IPv4/TCP/UDP/DNS/TLS frames
# so the self-test can verify parsing without requiring an external
# capture file.
# ===========================================================================

def build_eth(payload, ethertype=0x0800):
    """Wrap a payload in a minimal Ethernet II header with dummy MACs."""
    return (
        b"\x00\x11\x22\x33\x44\x55"          # Destination MAC (dummy)
        + b"\x66\x77\x88\x99\xaa\xbb"        # Source MAC (dummy)
        + struct.pack("!H", ethertype)        # EtherType (default: IPv4)
        + payload
    )


def build_ipv4(src, dst, proto, payload, ttl=64):
    """
    Build a minimal IPv4 header (20 bytes, no options) with a correct
    header checksum.  The DF (Don't Fragment) flag is set.
    """
    version_ihl = 0x45       # Version 4, IHL 5 (20 bytes).
    tos = 0
    total_len = 20 + len(payload)
    identification = 0x1234
    flags_frag = 0x4000      # DF flag set, fragment offset 0.

    # First pass: checksum field is zero.
    header = struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl,
        tos,
        total_len,
        identification,
        flags_frag,
        ttl,
        proto,
        0,                    # Checksum placeholder.
        socket.inet_aton(src),
        socket.inet_aton(dst),
    )
    csum = ipv4_checksum(header)
    # Second pass: insert the computed checksum.
    header = struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl,
        tos,
        total_len,
        identification,
        flags_frag,
        ttl,
        proto,
        csum,
        socket.inet_aton(src),
        socket.inet_aton(dst),
    )
    return header + payload


def build_udp(sport, dport, payload):
    """Build a minimal UDP header (8 bytes).  Checksum is left as 0 (valid per RFC 768)."""
    length = 8 + len(payload)
    header = struct.pack("!HHHH", sport, dport, length, 0)
    return header + payload


def build_tcp(sport, dport, flags, payload=b""):
    """
    Build a minimal TCP header (20 bytes, no options).
    Sequence/ack numbers, window, checksum, and urgent pointer are
    set to fixed dummy values (sufficient for parsing tests).
    """
    seq = 1
    ack = 0
    data_offset = 5 << 4     # 5 x 32-bit words = 20 bytes, in the high nibble.
    window = 65535
    checksum = 0             # Not validated by the parser.
    urg = 0
    header = struct.pack(
        "!HHIIBBHHH",
        sport,
        dport,
        seq,
        ack,
        data_offset,
        flags,
        window,
        checksum,
        urg,
    )
    return header + payload


def build_dns_query(name, qtype=1, txid=0x1234):
    """
    Build a minimal DNS query message for the given domain name.
    Flags: RD (Recursion Desired) set.  One question, no answers.
    """
    flags = 0x0100  # RD=1, QR=0 (query).
    header = struct.pack("!HHHHHH", txid, flags, 1, 0, 0, 0)
    # Encode the domain name as a sequence of labels.
    q = b""
    for label in name.split("."):
        if label:
            encoded = label.encode()
            q += bytes([len(encoded)]) + encoded
    q += b"\x00"  # Root label terminator.
    q += struct.pack("!HH", qtype, 1)  # QTYPE + QCLASS (IN).
    return header + q


def build_tls_client_hello(sni):
    """
    Build a minimal TLS 1.2 ClientHello with a single SNI extension.
    Contains one cipher suite (TLS_RSA_WITH_AES_128_CBC_SHA, 0x002F)
    and null compression.  Sufficient for parse_tls() validation.
    """
    name = sni.encode()
    # SNI extension body: ServerNameListLength(2) + NameType(1) + NameLength(2) + Name.
    sni_ext_body = (
        struct.pack("!H", len(name) + 3)
        + struct.pack("!B", 0)              # name_type = host_name
        + struct.pack("!H", len(name))
        + name
    )
    # Extension header: type(2) + length(2).
    sni_ext = struct.pack("!HH", 0, len(sni_ext_body)) + sni_ext_body
    extensions = sni_ext

    # ClientHello body.
    client_hello = struct.pack("!H", 0x0303)   # Client version: TLS 1.2.
    client_hello += b"\x00" * 32               # 32-byte random.
    client_hello += struct.pack("!B", 0)       # Session ID length: 0.
    client_hello += struct.pack("!H", 2) + struct.pack("!H", 0x002F)  # 1 cipher suite.
    client_hello += struct.pack("!B", 1) + struct.pack("!B", 0)       # 1 compression: null.
    client_hello += struct.pack("!H", len(extensions)) + extensions   # Extensions block.

    # Handshake header: type(1) + length(3).
    handshake = struct.pack("!B", 1) + len(client_hello).to_bytes(3, "big") + client_hello
    # TLS record header: content_type(1) + version(2) + length(2).
    record = struct.pack("!BHH", 0x16, 0x0301, len(handshake)) + handshake
    return record


def write_pcap(path, packets):
    """
    Write a list of raw Ethernet frames to a classic pcap file.
    Uses little-endian byte order, microsecond timestamps, and
    linktype 1 (Ethernet).  Timestamps start at 1700000000 (2023-11-14)
    and increment by 1 second per packet.
    """
    with open(path, "wb") as f:
        # Global header: magic, version 2.4, thiszone=0, sigfigs=0, snaplen=65535, network=1.
        f.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
        ts = 1700000000
        for i, pkt in enumerate(packets):
            # Per-packet record header: ts_sec, ts_usec, incl_len, orig_len.
            f.write(struct.pack("<IIII", ts + i, i * 1000, len(pkt), len(pkt)))
            f.write(pkt)


# ===========================================================================
# Self-test: generates a synthetic pcap in a temp directory, runs the
# full analysis pipeline, and asserts that each parser produced the
# expected output.  Returns 0 on success, 1 on failure.
# Can output results as JSON (--json) for CI integration.
# ===========================================================================
def run_self_test(painter, as_json=False):
    if not as_json:
        print_banner(painter, "SELF TEST")

    tmpdir = tempfile.mkdtemp(prefix="pcap_analyzer_")
    pcap_path = os.path.join(tmpdir, "test.pcap")

    try:
        # --- Construct test payloads ---

        # HTTP GET with a Basic Authorization header (user:pass in base64).
        http_payload = (
            b"GET /login?user=admin HTTP/1.1\r\n"
            b"Host: ctf.local\r\n"
            b"Authorization: Basic dXNlcjpwYXNz\r\n"  # base64("user:pass")
            b"User-Agent: pcap-analyzer-self-test\r\n"
            b"\r\n"
        )

        # TLS ClientHello with SNI "ctf.example".
        tls_payload = build_tls_client_hello("ctf.example")

        # Four test packets covering DNS, HTTP, TLS, and a bare TCP SYN.
        packets = [
            # 1. DNS query for example.com (UDP port 53).
            build_eth(build_ipv4("10.0.0.2", "10.0.0.1", 17,
                                 build_udp(5555, 53, build_dns_query("example.com")))),
            # 2. HTTP GET with Basic auth (TCP port 80, PSH+ACK flags).
            build_eth(build_ipv4("10.0.0.2", "93.184.216.34", 6,
                                 build_tcp(5556, 80, 0x18, http_payload))),
            # 3. TLS ClientHello (TCP port 443, PSH+ACK flags).
            build_eth(build_ipv4("10.0.0.2", "93.184.216.34", 6,
                                 build_tcp(5557, 443, 0x18, tls_payload))),
            # 4. Bare TCP SYN (no payload) to trigger SYN-without-ACK counter.
            build_eth(build_ipv4("10.0.0.2", "10.0.0.99", 6,
                                 build_tcp(5558, 80, 0x02))),
        ]

        write_pcap(pcap_path, packets)

        # --- Run full analysis ---
        analyzer = Analyzer(set(FEATURES), limit=10, reveal=False)
        file_type, gen = iter_packets(pcap_path)
        analyzer.file_type = file_type
        for ts, caplen, origlen, data, linktype in gen:
            analyzer.process_packet(ts, caplen, origlen, data, linktype)

        report = analyzer.report()
        checks = []

        def check(name, condition):
            """Record a named assertion for later reporting."""
            checks.append((name, bool(condition)))

        # --- Assertions ---
        check("File type is pcap", report["file_type"] == "pcap")
        check("Packet count is 4", report["summary"]["packet_count"] == 4)
        check("DNS query parsed", report["dns"]["query_count"] >= 1)
        check(
            "DNS example.com present",
            any("example.com" in q.get("query", "") for q in report["dns"]["queries"]),
        )
        check("HTTP request parsed", report["http"]["request_count"] >= 1)
        check("HTTP Basic credential detected", report["creds"]["count"] >= 1)
        check(
            "TLS SNI parsed",
            any(e.get("sni") == "ctf.example" for e in report["tls"]["events"]),
        )
        check(
            "TCP SYN count present",
            report["anomalies"]["counts"].get("TCP SYN without ACK", 0) >= 1,
        )

        # --- Verify feature gating: disabling DNS should remove the DNS section ---
        analyzer2 = Analyzer(set(FEATURES) - {"dns"}, limit=10, reveal=False)
        file_type2, gen2 = iter_packets(pcap_path)
        analyzer2.file_type = file_type2
        for ts, caplen, origlen, data, linktype in gen2:
            analyzer2.process_packet(ts, caplen, origlen, data, linktype)

        report2 = analyzer2.report()
        check("Skip DNS removes DNS section", report2["dns"] is None)

        # --- Output results ---
        if as_json:
            print(json.dumps({"checks": checks, "report1": report, "report2": report2}, indent=2, default=str))
            failed = [name for name, ok in checks if not ok]
            if failed:
                return 1
            return 0

        rows = [(name, "PASS" if ok else "FAIL") for name, ok in checks]
        colors = ["green" if ok else "red" for _, ok in checks]
        print_section(painter, "Self Test Results",
                      render_table(painter, ["Check", "Result"], rows, colors))

        failed = [name for name, ok in checks if not ok]
        if failed:
            print(painter.paint(f"Failed checks: {', '.join(failed)}", "red"))
            return 1

        print(painter.paint("All self-test checks passed.", "bold", "green"))
        return 0

    except Exception as exc:
        if as_json:
            print(json.dumps({"error": str(exc)}))
        else:
            print(painter.paint(f"Self-test exception: {exc}", "red"))
        return 1

    finally:
        # Clean up the temporary pcap file and directory.
        try:
            os.unlink(pcap_path)
        except OSError:
            pass
        try:
            os.rmdir(tmpdir)
        except OSError:
            pass


# ===========================================================================
# CLI entry point.
# Parses arguments, configures the Painter, selects features, opens the
# capture file, runs the analysis, and outputs the report.
# ===========================================================================
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Standard-library PCAP/PCAPNG analyzer for defensive research and CTF triage.",
    )
    parser.add_argument("pcap", nargs="?", help="Path to pcap or pcapng file")
    parser.add_argument("--self-test", action="store_true", help="Generate a test pcap and verify core parsing")
    parser.add_argument("--only", help="Comma-separated features to run")
    parser.add_argument("--skip", help="Comma-separated features to skip")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactively choose features")
    parser.add_argument("--limit", type=int, default=20, help="Maximum stored events per section")
    parser.add_argument("--reveal-secrets", action="store_true", help="Do not redact discovered secrets")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    args = parser.parse_args(argv)

    # Determine whether to emit ANSI color codes.
    # Disabled when: --no-color, --json, NO_COLOR env var, or stdout is not a TTY.
    color_enabled = (
        not args.no_color
        and not args.json
        and os.environ.get("NO_COLOR") is None
        and sys.stdout.isatty()
    )
    painter = Painter(color_enabled)

    # Self-test mode: no input file required.
    if args.self_test:
        return run_self_test(painter, args.json)

    if not args.pcap:
        parser.error("Provide a pcap/pcapng file or use --self-test.")

    # Feature selection: --only overrides the default (all features).
    if args.only:
        try:
            selected = parse_feature_list(args.only)
        except ValueError as exc:
            parser.error(str(exc))
    elif args.interactive:
        selected = interactive_select(painter)
    else:
        selected = set(FEATURES)  # Default: all features enabled.

    # --skip removes features from the selected set.
    if args.skip:
        try:
            skip = parse_feature_list(args.skip)
        except ValueError as exc:
            parser.error(str(exc))
        selected -= skip

    if not selected:
        parser.error("No features selected.")

    if not os.path.isfile(args.pcap):
        parser.error(f"File not found: {args.pcap}")

    analyzer = Analyzer(selected, limit=args.limit, reveal=args.reveal_secrets)

    try:
        file_type, packets = iter_packets(args.pcap)
        analyzer.file_type = file_type
        # Main processing loop: iterate over every packet in the capture.
        for ts, caplen, origlen, data, linktype in packets:
            analyzer.process_packet(ts, caplen, origlen, data, linktype)
    except Exception as exc:
        print(painter.paint(f"Error analyzing file: {exc}", "red"), file=sys.stderr)
        return 1

    # Output: JSON (machine-readable) or formatted tables (human-readable).
    if args.json:
        print(json.dumps(analyzer.report(), indent=2, default=str))
    else:
        print_report(analyzer, painter)

    return 0


if __name__ == "__main__":
    sys.exit(main())
