#!/bin/bash
#===============================================================================
# EasyScan v2 - A kinda simple CTF Reconnaissance & Scanning Suite 
# News: wordlist auto-detect, silent-skip elimination, output validation,
#        dirsearch python compat, parallel job error capture
# Author: Maat
#===============================================================================

set -uo pipefail

#--- Configuration -------------------------------------------------------------
readonly SCRIPT_VERSION="3.1"
readonly SCAN_BASE_DIR="${HOME}/Documents/Scans"
readonly GOBUSTER_THREADS=50
readonly FFUF_RATE=500
readonly FFUF_RECURSION_DEPTH=3
readonly NMAP_TIMEOUT="--host-timeout 300s"
readonly MAX_PARALLEL=4
readonly STATE_FILE_EXT=".easyscan_state"
readonly GOWITNESS_TIMEOUT=15
readonly FILE_EXTENSIONS=".html,.php,.txt,.bak,.conf,.log,.xml,.json,.asp,.aspx,.jsp"

#--- Color and Formatting ------------------------------------------------------
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly MAGENTA='\033[0;35m'
readonly BOLD='\033[1m'
readonly DIM='\033[2m'
readonly NC='\033[0m'

#--- Global State --------------------------------------------------------------
declare -a JOB_PIDS=()
declare -a HTTP_PORTS=()
declare -a HTTPS_PORTS=()
declare -a ALL_OPEN_PORTS=()
declare -A PORT_SERVICES=()
TARGET_IP=""
TARGET_DOMAIN=""
REPORT_FORMAT="markdown"
NMAP_OUTPUT_FILE=""
GOBUSTER_OUTPUT_FILE=""
NIKTO_OUTPUT_FILE=""
DIRSEARCH_OUTPUT_FILE=""
FFUF_OUTPUT_FILE=""
WPSCAN_OUTPUT_FILE=""
GOWITNESS_DIR=""
STATE_FILE=""
SCAN_ID=""

# FIX: Wordlist paths are now resolved dynamically, not hardcoded.
# These variables are populated by detect_wordlists().
WL_DIR_COMMON=""
WL_DIR_MEDIUM=""
WL_DIR_BIG=""
WL_DNS_SUB=""
WL_DNS_NAM=""

#--- Utility Functions ---------------------------------------------------------

log_info()    { echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} ${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} ${GREEN}[ OK ]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[$(date +%H:%M:%S)]${NC} ${YELLOW}[WARN]${NC} $*"; }
log_error()   { echo -e "${RED}[$(date +%H:%M:%S)]${NC} ${RED}[ERR ]${NC} $*" >&2; }
log_phase()   { echo -e "\n${BOLD}${MAGENTA}>>> PHASE: $*${NC}\n"; }
log_header()  {
    echo -e "\n${BOLD}${CYAN}══════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}  $*${NC}"
    echo -e "${BOLD}${CYAN}══════════════════════════════════════════════════════════${NC}\n"
}

die() { log_error "$*"; cleanup_all; exit 1; }
timestamp() { date '+%Y%m%d_%H%M%S'; }

validate_ip() {
    local ip="$1"
    [[ "$ip" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1
    local IFS='.'
    read -r -a octets <<< "$ip"
    for octet in "${octets[@]}"; do (( octet <= 255 )) || return 1; done
    return 0
}

validate_domain() {
    [[ "$1" =~ ^[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$ ]]
}

prompt_read() {
    local prompt="$1" var_name="$2"
    echo -en "${BOLD}${prompt}${NC}"
    read -r "$var_name"
}

command_exists() { command -v "$1" &>/dev/null; }

#--- FIX: Wordlist Auto-Detection ----------------------------------------------
# Searches multiple known locations (case variations included) and resolves
# the first match. Dies loudly if a critical wordlist cannot be found.

find_wordlist() {
    # $1 = description, $2..$N = candidate paths
    local desc="$1"; shift
    local candidates=("$@")
    for path in "${candidates[@]}"; do
        if [[ -f "$path" ]]; then
            echo "$path"
            return 0
        fi
    done
    # FIX: Also try a case-insensitive find as last resort
    local base_name
    base_name=$(basename "${candidates[0]}")
    local search_dirs=("/usr/share/wordlists" "/usr/share/seclists" "/usr/share/SecLists" "/opt/SecLists" "/usr/share/dirbuster")
    for sdir in "${search_dirs[@]}"; do
        if [[ -d "$sdir" ]]; then
            local found
            found=$(find "$sdir" -iname "$base_name" -type f 2>/dev/null | head -1)
            if [[ -n "$found" ]]; then
                echo "$found"
                return 0
            fi
        fi
    done
    return 1
}

detect_wordlists() {
    log_header "Wordlist Auto-Detection"

    # Directory brute-force: common
    WL_DIR_COMMON=$(find_wordlist "dir-common" \
        "/usr/share/wordlists/dirb/common.txt" \
        "/usr/share/seclists/Discovery/Web-Content/common.txt" \
        "/usr/share/SecLists/Discovery/Web-Content/common.txt" \
        "/usr/share/dirbuster/wordlists/directory-list-2.3-small.txt" \
    ) || true

    # Directory brute-force: medium
    WL_DIR_MEDIUM=$(find_wordlist "dir-medium" \
        "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt" \
        "/usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt" \
        "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt" \
        "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt" \
    ) || true

    # Directory brute-force: big (fallback for dirsearch)
    WL_DIR_BIG=$(find_wordlist "dir-big" \
        "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-big.txt" \
        "/usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt" \
        "/usr/share/wordlists/dirbuster/directory-list-2.3-big.txt" \
    ) || true

    # DNS subdomains
    WL_DNS_SUB=$(find_wordlist "dns-sub" \
        "/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt" \
        "/usr/share/SecLists/Discovery/DNS/subdomains-top1million-20000.txt" \
        "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt" \
    ) || true

    # Report findings
    local critical_missing=0

    if [[ -n "$WL_DIR_COMMON" ]]; then
        log_success "Dir common:  $WL_DIR_COMMON"
    else
        log_error "Dir common wordlist NOT FOUND (gobuster/ffuf will fail)"
        critical_missing=1
    fi

    if [[ -n "$WL_DIR_MEDIUM" ]]; then
        log_success "Dir medium:  $WL_DIR_MEDIUM"
    else
        log_warn "Dir medium wordlist not found (will fall back to common)"
        WL_DIR_MEDIUM="$WL_DIR_COMMON"   # FIX: graceful fallback
    fi

    if [[ -n "$WL_DIR_BIG" ]]; then
        log_success "Dir big:     $WL_DIR_BIG"
    else
        log_warn "Dir big wordlist not found (dirsearch will use medium)"
        WL_DIR_BIG="$WL_DIR_MEDIUM"
    fi

    if [[ -n "$WL_DNS_SUB" ]]; then
        log_success "DNS sub:     $WL_DNS_SUB"
    else
        log_warn "DNS subdomain wordlist not found (DNS enum will be skipped)"
    fi

    # FIX: Die loudly if we cannot do any directory brute-forcing at all
    if (( critical_missing )) && [[ -z "$WL_DIR_MEDIUM" ]]; then
        die "No directory wordlists found. Install seclists: sudo apt install -y seclists"
    fi
}

#--- Parallel Job Control ------------------------------------------------------

run_parallel() {
    local description="$1"; shift
    local cmd=("$@")

    while (( ${#JOB_PIDS[@]} >= MAX_PARALLEL )); do
        local new_pids=()
        for pid in "${JOB_PIDS[@]}"; do
            kill -0 "$pid" 2>/dev/null && new_pids+=("$pid")
        done
        JOB_PIDS=("${new_pids[@]}")
        (( ${#JOB_PIDS[@]} >= MAX_PARALLEL )) && sleep 1
    done

    log_info "${DIM}[BG] Starting: ${description}${NC}"

    # FIX: Capture stderr alongside stdout so errors are visible in logs
    local log_file="${SCAN_BASE_DIR}/.joblogs/$(echo "$description" | tr ' /:' '___')_$(timestamp).log"
    mkdir -p "${SCAN_BASE_DIR}/.joblogs"
    "${cmd[@]}" > "$log_file" 2>&1 &
    local pid=$!
    JOB_PIDS+=("$pid")
    log_info "${DIM}[BG] PID ${pid}: ${description} -> $(basename "$log_file")${NC}"
}

wait_all_jobs() {
    if (( ${#JOB_PIDS[@]} > 0 )); then
        log_info "Waiting for ${#JOB_PIDS[@]} background job(s)..."
        local failed=0
        for pid in "${JOB_PIDS[@]}"; do
            if ! wait "$pid" 2>/dev/null; then
                ((failed++))
            fi
        done
        JOB_PIDS=()
        if (( failed > 0 )); then
            log_warn "${failed} job(s) exited with errors. Check ${SCAN_BASE_DIR}/.joblogs/"
        else
            log_success "All parallel jobs finished"
        fi
    fi
}

kill_all_jobs() {
    for pid in "${JOB_PIDS[@]}"; do kill "$pid" 2>/dev/null || true; done
    JOB_PIDS=()
}

#--- State Management (Resume) -------------------------------------------------

init_state() {
    SCAN_ID="${TARGET_IP}_$(timestamp)"
    STATE_FILE="${SCAN_BASE_DIR}/.state/${SCAN_ID}${STATE_FILE_EXT}"
    mkdir -p "${SCAN_BASE_DIR}/.state"

    local existing_state
    existing_state=$(ls -t "${SCAN_BASE_DIR}/.state/${TARGET_IP}_"*"${STATE_FILE_EXT}" 2>/dev/null | head -1)

    if [[ -n "$existing_state" && -f "$existing_state" ]]; then
        log_warn "Previous scan state found: $(basename "$existing_state")"
        prompt_read "Resume previous scan? [yes/no]: " resume_choice
        if [[ "$resume_choice" == "yes" ]]; then
            STATE_FILE="$existing_state"
            SCAN_ID=$(basename "$STATE_FILE" "$STATE_FILE_EXT")
            load_state
            return 0
        fi
    fi

    cat > "$STATE_FILE" << EOF
{
  "scan_id": "${SCAN_ID}",
  "target_ip": "${TARGET_IP}",
  "target_domain": "${TARGET_DOMAIN}",
  "report_format": "${REPORT_FORMAT}",
  "started_at": "$(date -Iseconds)",
  "phases": {
    "nmap": "pending",
    "port_extract": "pending",
    "gobuster": "pending",
    "ffuf": "pending",
    "gowitness": "pending",
    "port_services": "pending",
    "nikto": "pending",
    "wpscan": "pending",
    "dirsearch": "pending",
    "report": "pending"
  },
  "http_ports": "",
  "https_ports": "",
  "all_ports": "",
  "nmap_file": "",
  "completed_at": ""
}
EOF
    log_info "New scan state initialized: ${SCAN_ID}"
}

load_state() {
    log_info "Loading previous state..."
    TARGET_IP=$(grep '"target_ip"' "$STATE_FILE" | sed 's/.*: *"//;s/".*//')
    TARGET_DOMAIN=$(grep '"target_domain"' "$STATE_FILE" | sed 's/.*: *"//;s/".*//')
    REPORT_FORMAT=$(grep '"report_format"' "$STATE_FILE" | sed 's/.*: *"//;s/".*//')
    NMAP_OUTPUT_FILE=$(grep '"nmap_file"' "$STATE_FILE" | sed 's/.*: *"//;s/".*//')
    local ports_str
    ports_str=$(grep '"http_ports"' "$STATE_FILE" | sed 's/.*: *"//;s/".*//')
    IFS=',' read -r -a HTTP_PORTS <<< "$ports_str" 2>/dev/null || HTTP_PORTS=()
    ports_str=$(grep '"https_ports"' "$STATE_FILE" | sed 's/.*: *"//;s/".*//')
    IFS=',' read -r -a HTTPS_PORTS <<< "$ports_str" 2>/dev/null || HTTPS_PORTS=()
    ports_str=$(grep '"all_ports"' "$STATE_FILE" | sed 's/.*: *"//;s/".*//')
    IFS=',' read -r -a ALL_OPEN_PORTS <<< "$ports_str" 2>/dev/null || ALL_OPEN_PORTS=()
    log_success "State loaded. Resuming scan for ${TARGET_IP}"
}

update_phase() {
    sed -i "s/\"$1\": *\"[a-z]*\"/\"$1\": \"$2\"/" "$STATE_FILE"
}

update_state_field() {
    sed -i "s|\"$1\": *\"[^\"]*\"|\"$1\": \"$2\"|" "$STATE_FILE"
}

phase_completed() { grep -q "\"$1\": *\"done\"" "$STATE_FILE" 2>/dev/null; }
phase_skipped()   { grep -q "\"$1\": *\"skipped\"" "$STATE_FILE" 2>/dev/null; }

should_run_phase() {
    if phase_completed "$1" || phase_skipped "$1"; then
        log_info "Phase '$1' already complete/skipped. Skipping."
        return 1
    fi
    return 0
}

#--- Banner --------------------------------------------------------------------
show_banner() {
    if command_exists figlet; then
        local tw; tw=$(tput cols 2>/dev/null || echo 80)
        figlet -f slant "EasyScan v3" 2>/dev/null | \
            awk -v tw="$tw" '{printf "%-*s\n", int((tw-length($0))/2), $0}'
    else
        cat << 'BANNER'
   ______                _____
  / ____/___  ____ _____/ ___/____ ______________
 / __/ / __ `/ __ `/ __ \__ \/ __ `/ ___/ ___/ _ \
/ /___/ /_/ / /_/ / / / /__/ / /_/ / /__/ /  /  __/
\____/\__,_/\__,_/_/ /_/____/\__,_/\___/_/   \___/
BANNER
    fi
    echo -e "${YELLOW}  v${SCRIPT_VERSION} | Parallel CTF Recon Suite${NC}"
    echo -e "${DIM}  nmap + gobuster + ffuf + nikto + wpscan + dirsearch + gowitness${NC}\n"
}

#--- Tool Verification ---------------------------------------------------------
check_tools() {
    log_header "Tool Verification"

    local required=("nmap" "gobuster" "ffuf")
    local optional=("nikto" "wpscan" "dirsearch" "gowitness" "enum4linux" "smbclient" "nbtscan" "snmpwalk" "showmount" "rpcinfo" "smtp-user-enum")
    local missing_req=()

    for tool in "${required[@]}"; do
        if command_exists "$tool"; then
            log_success "  $tool -> $(command -v "$tool")"
        else
            log_error "  $tool NOT FOUND (REQUIRED)"
            missing_req+=("$tool")
        fi
    done

    for tool in "${optional[@]}"; do
        command_exists "$tool" && log_success "  $tool" || log_warn "  $tool (optional, some enums skipped)"
    done

    if (( ${#missing_req[@]} > 0 )); then
        prompt_read "Install missing required tools? [yes/no]: " choice
        if [[ "$choice" == "yes" ]]; then
            for tool in "${missing_req[@]}"; do
                sudo apt install -y "$tool" 2>/dev/null && log_success "$tool installed" || log_error "Failed: $tool"
            done
        fi
    fi

    command_exists nmap || die "nmap is mandatory."
    command_exists gobuster || die "gobuster is mandatory."
    command_exists ffuf || die "ffuf is mandatory."

    # FIX: Check dirsearch python compatibility
    if command_exists dirsearch; then
        if ! dirsearch --version &>/dev/null; then
            log_warn "dirsearch found but broken (likely missing pkg_resources on Python 3.12+)"
            log_info "Fix: pip install setuptools  OR  pipx install dirsearch"
            prompt_read "Attempt 'sudo pip install setuptools' now? [yes/no]: " fix_choice
            if [[ "$fix_choice" == "yes" ]]; then
                sudo pip install setuptools 2>/dev/null || sudo pip3 install setuptools 2>/dev/null || true
                if dirsearch --version &>/dev/null; then
                    log_success "dirsearch fixed"
                else
                    log_warn "dirsearch still broken, will be skipped"
                fi
            fi
        fi
    fi
}

#--- Directory Setup -----------------------------------------------------------
setup_directories() {
    local subdirs=("nmap" "gobuster" "nikto" "dirsearch" "ffuf" "wpscan" "gowitness" "port_services" "Reports" ".state" ".joblogs")
    for dir in "${subdirs[@]}"; do mkdir -p "${SCAN_BASE_DIR}/${dir}"; done
    GOWITNESS_DIR="${SCAN_BASE_DIR}/gowitness/${TARGET_IP}"
    mkdir -p "$GOWITNESS_DIR"
}

#--- Hosts File ----------------------------------------------------------------
add_to_hosts() {
    local entry="${TARGET_IP} ${TARGET_DOMAIN}"
    grep -qF "$entry" /etc/hosts 2>/dev/null && { log_info "Already in /etc/hosts: $entry"; return 0; }
    echo "$entry" | sudo tee -a /etc/hosts > /dev/null
    log_success "Added to /etc/hosts: $entry"
}

#--- Phase 1: Nmap -------------------------------------------------------------
run_nmap() {
    should_run_phase "nmap" || return 0
    update_phase "nmap" "running"
    log_phase "NMAP PORT SCAN"

    echo "  1) Common ports (-sV, top 1000)"
    echo "  2) All 65535 ports (-sV -p-)"
    echo "  3) Quick SYN (-sS, top 1000, no version)"
    echo "  4) UDP top 100 + TCP common"
    prompt_read "Select mode [1-4]: " nmap_mode

    local nmap_base="${SCAN_BASE_DIR}/nmap/nmap_${TARGET_IP}"
    local nmap_cmd=""
    case "$nmap_mode" in
        1) nmap_cmd="sudo nmap -sV -vv ${NMAP_TIMEOUT} -oA ${nmap_base} ${TARGET_IP}" ;;
        2) nmap_cmd="sudo nmap -sV -vv -p- ${NMAP_TIMEOUT} -oA ${nmap_base} ${TARGET_IP}" ;;
        3) nmap_cmd="sudo nmap -sS -vv ${NMAP_TIMEOUT} -oA ${nmap_base} ${TARGET_IP}" ;;
        4) nmap_cmd="sudo nmap -sV -sU --top-ports 100 -vv ${NMAP_TIMEOUT} -oA ${nmap_base} ${TARGET_IP}" ;;
        *) nmap_cmd="sudo nmap -sV -vv ${NMAP_TIMEOUT} -oA ${nmap_base} ${TARGET_IP}" ;;
    esac

    log_info "Running: $nmap_cmd"
    eval "$nmap_cmd" 2>&1 | tee "${nmap_base}_console.txt"

    # FIX: Prefer the .nmap grepable output for reliable parsing
    if [[ -f "${nmap_base}.nmap" ]]; then
        NMAP_OUTPUT_FILE="${nmap_base}.nmap"
    else
        NMAP_OUTPUT_FILE="${nmap_base}_console.txt"
    fi

    update_state_field "nmap_file" "$NMAP_OUTPUT_FILE"
    update_phase "nmap" "done"
    log_success "Nmap complete: $NMAP_OUTPUT_FILE"
}

#--- Phase 2: Extract Ports ----------------------------------------------------
extract_ports() {
    should_run_phase "port_extract" || return 0
    update_phase "port_extract" "running"
    log_phase "PORT EXTRACTION"

    HTTP_PORTS=(); HTTPS_PORTS=(); ALL_OPEN_PORTS=()

    [[ -f "$NMAP_OUTPUT_FILE" ]] || { log_error "Nmap file missing"; update_phase "port_extract" "done"; return 1; }

    while IFS= read -r line; do
        local port; port=$(echo "$line" | awk '{print $1}' | cut -d'/' -f1)
        [[ -n "$port" ]] && ALL_OPEN_PORTS+=("$port")
    done < <(grep -E '^[0-9]+/tcp\s+open' "$NMAP_OUTPUT_FILE" 2>/dev/null || true)

    while IFS= read -r line; do
        local port; port=$(echo "$line" | awk '{print $1}' | cut -d'/' -f1)
        [[ -n "$port" ]] && HTTP_PORTS+=("$port")
    done < <(grep -E '^[0-9]+/tcp\s+open\s+(http|http-alt|http-proxy|vnc-http)' "$NMAP_OUTPUT_FILE" 2>/dev/null || true)

    while IFS= read -r line; do
        local port; port=$(echo "$line" | awk '{print $1}' | cut -d'/' -f1)
        [[ -n "$port" ]] && HTTPS_PORTS+=("$port")
    done < <(grep -E '^[0-9]+/tcp\s+open\s+ssl/(http|https)' "$NMAP_OUTPUT_FILE" 2>/dev/null || true)

    update_state_field "http_ports" "$(IFS=','; echo "${HTTP_PORTS[*]}")"
    update_state_field "https_ports" "$(IFS=','; echo "${HTTPS_PORTS[*]}")"
    update_state_field "all_ports" "$(IFS=','; echo "${ALL_OPEN_PORTS[*]}")"

    log_info "All open TCP: ${ALL_OPEN_PORTS[*]:-none}"
    log_info "HTTP:  ${HTTP_PORTS[*]:-none}"
    log_info "HTTPS: ${HTTPS_PORTS[*]:-none}"
    update_phase "port_extract" "done"
}

#--- Phase 3: Gobuster (Parallel) ----------------------------------------------
run_gobuster() {
    should_run_phase "gobuster" || return 0
    update_phase "gobuster" "running"
    log_phase "GOBUSTER ENUMERATION (Parallel)"

    # FIX: Validate wordlist BEFORE entering port loops
    if [[ -z "$WL_DIR_COMMON" ]]; then
        log_error "No directory wordlist available. Cannot run gobuster."
        update_phase "gobuster" "skipped"
        return 1
    fi

    local out_base="${SCAN_BASE_DIR}/gobuster/gobuster_${TARGET_IP}_$(timestamp)"
    local jobs_launched=0

    for port in "${HTTP_PORTS[@]}"; do
        log_info "Launching gobuster dir -> http://${TARGET_IP}:${port}/ (wordlist: $(basename "$WL_DIR_COMMON"))"
        run_parallel "gobuster_dir_http_${port}" \
            gobuster dir \
                -u "http://${TARGET_IP}:${port}/" \
                -w "$WL_DIR_COMMON" \
                -t "$GOBUSTER_THREADS" \
                --no-error \
                -x php,html,txt,bak,conf \
                -o "${out_base}_dir_http_${port}.txt"
        ((jobs_launched++))
    done

    for port in "${HTTPS_PORTS[@]}"; do
        local wl_https="${WL_DIR_MEDIUM:-$WL_DIR_COMMON}"
        log_info "Launching gobuster dir -> https://${TARGET_IP}:${port}/ (wordlist: $(basename "$wl_https"))"
        run_parallel "gobuster_dir_https_${port}" \
            gobuster dir \
                -u "https://${TARGET_IP}:${port}/" \
                -w "$wl_https" \
                -t "$GOBUSTER_THREADS" \
                -k --no-error \
                -x php,html,txt,bak,conf \
                -o "${out_base}_dir_https_${port}.txt"
        ((jobs_launched++))
    done

    if [[ -n "$TARGET_DOMAIN" && -n "$WL_DNS_SUB" ]]; then
        run_parallel "gobuster_dns_${TARGET_DOMAIN}" \
            gobuster dns -d "$TARGET_DOMAIN" -w "$WL_DNS_SUB" -t "$GOBUSTER_THREADS" --no-error \
                -o "${out_base}_dns.txt"
        ((jobs_launched++))

        run_parallel "gobuster_vhost_${TARGET_DOMAIN}" \
            gobuster vhost -u "http://${TARGET_DOMAIN}" -w "$WL_DNS_SUB" -t "$GOBUSTER_THREADS" \
                --append-domain --no-error -o "${out_base}_vhost.txt"
        ((jobs_launched++))
    fi

    # FIX: Check if any jobs were actually launched
    if (( jobs_launched == 0 )); then
        log_warn "No gobuster jobs launched (no web ports or missing wordlists)"
        update_phase "gobuster" "skipped"
        return 0
    fi

    wait_all_jobs

    GOBUSTER_OUTPUT_FILE="${out_base}_merged.txt"
    cat "${out_base}"_*.txt > "$GOBUSTER_OUTPUT_FILE" 2>/dev/null || true

    # FIX: Validate output is non-empty
    if [[ ! -s "$GOBUSTER_OUTPUT_FILE" ]]; then
        log_warn "Gobuster merged output is EMPTY. Check job logs in ${SCAN_BASE_DIR}/.joblogs/"
    else
        log_success "Gobuster found $(wc -l < "$GOBUSTER_OUTPUT_FILE") line(s)"
    fi

    update_phase "gobuster" "done"
    log_success "Gobuster complete: $GOBUSTER_OUTPUT_FILE"
}

#--- Phase 4: FFuF Recursive (Parallel) ----------------------------------------
run_ffuf() {
    should_run_phase "ffuf" || return 0
    update_phase "ffuf" "running"
    log_phase "FFUF RECURSIVE FUZZING (Parallel)"

    if ! command_exists ffuf; then
        log_warn "ffuf not available"
        update_phase "ffuf" "skipped"
        return 0
    fi

    # FIX: Use resolved wordlist, fall back to common if medium missing
    local ffuf_wl="${WL_DIR_MEDIUM:-$WL_DIR_COMMON}"
    if [[ -z "$ffuf_wl" || ! -f "$ffuf_wl" ]]; then
        log_error "No wordlist for ffuf. Skipping."
        update_phase "ffuf" "skipped"
        return 1
    fi

    log_info "FFuF wordlist: $ffuf_wl"
    local out_base="${SCAN_BASE_DIR}/ffuf/ffuf_${TARGET_IP}_$(timestamp)"
    local jobs_launched=0

    for port in "${HTTP_PORTS[@]}"; do
        log_info "Launching ffuf -> http://${TARGET_IP}:${port}/FUZZ"
        run_parallel "ffuf_http_${port}" \
            ffuf \
                -w "$ffuf_wl" \
                -u "http://${TARGET_IP}:${port}/FUZZ" \
                -e "$FILE_EXTENSIONS" \
                -recursion -recursion-depth "$FFUF_RECURSION_DEPTH" \
                -rate "$FFUF_RATE" \
                -fc 404 -ic \
                -o "${out_base}_http_${port}.json" -of json
        ((jobs_launched++))
    done

    for port in "${HTTPS_PORTS[@]}"; do
        log_info "Launching ffuf -> https://${TARGET_IP}:${port}/FUZZ"
        run_parallel "ffuf_https_${port}" \
            ffuf \
                -w "$ffuf_wl" \
                -u "https://${TARGET_IP}:${port}/FUZZ" \
                -e "$FILE_EXTENSIONS" \
                -recursion -recursion-depth "$FFUF_RECURSION_DEPTH" \
                -rate "$FFUF_RATE" \
                -fc 404 -ic \
                -o "${out_base}_https_${port}.json" -of json
        ((jobs_launched++))
    done

    if (( jobs_launched == 0 )); then
        log_warn "No ffuf jobs launched (no web ports)"
        update_phase "ffuf" "skipped"
        return 0
    fi

    wait_all_jobs

    # Build readable summary from JSON outputs
    local readable="${out_base}_readable.txt"
    > "$readable"
    for f in "${out_base}"_*.json; do
        [[ -f "$f" ]] || continue
        echo "--- $(basename "$f") ---" >> "$readable"
        grep -o '"url":"[^"]*"' "$f" 2>/dev/null | sed 's/"url":"//;s/"//' >> "$readable" || true
        echo "" >> "$readable"
    done
    FFUF_OUTPUT_FILE="$readable"

    if [[ ! -s "$FFUF_OUTPUT_FILE" ]]; then
        log_warn "FFuF output is EMPTY. Check job logs."
    else
        log_success "FFuF found $(grep -c 'http' "$FFUF_OUTPUT_FILE" 2>/dev/null || echo 0) URL(s)"
    fi

    update_phase "ffuf" "done"
}

#--- Phase 5: Gowitness --------------------------------------------------------
run_gowitness() {
    should_run_phase "gowitness" || return 0
    update_phase "gowitness" "running"
    log_phase "GOWITNESS SCREENSHOTS"

    if ! command_exists gowitness; then
        log_warn "gowitness not available, skipping"
        update_phase "gowitness" "skipped"
        return 0
    fi

    local url_file="${GOWITNESS_DIR}/urls.txt"
    > "$url_file"
    for port in "${HTTP_PORTS[@]}";  do echo "http://${TARGET_IP}:${port}"  >> "$url_file"; done
    for port in "${HTTPS_PORTS[@]}"; do echo "https://${TARGET_IP}:${port}" >> "$url_file"; done

    if [[ -s "$url_file" ]]; then
        gowitness file -f "$url_file" --destination "$GOWITNESS_DIR" \
            --timeout "$GOWITNESS_TIMEOUT" --threads "$MAX_PARALLEL" 2>/dev/null \
            || log_warn "gowitness had errors"
        log_success "Screenshots: $GOWITNESS_DIR"
    fi
    update_phase "gowitness" "done"
}

#--- Phase 6: Port-Specific Service Enumeration --------------------------------
run_port_services() {
    should_run_phase "port_services" || return 0
    update_phase "port_services" "running"
    log_phase "PORT-SPECIFIC SERVICE ENUMERATION (Parallel)"

    local out_base="${SCAN_BASE_DIR}/port_services/${TARGET_IP}"
    mkdir -p "$out_base"

    for port in "${ALL_OPEN_PORTS[@]}"; do
        local service
        service=$(grep "^${port}/" "$NMAP_OUTPUT_FILE" 2>/dev/null | awk '{print $3}' | head -1)
        PORT_SERVICES[$port]="${service:-unknown}"

        case "$port" in
            21)
                run_parallel "FTP_enum_${port}" bash -c "
                    { echo '=== FTP ANON CHECK ===';
                      nmap --script ftp-anon,ftp-bounce -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/ftp_${port}.txt' 2>&1"
                ;;
            22)
                run_parallel "SSH_enum_${port}" bash -c "
                    { echo '=== SSH BANNER ===';
                      timeout 5 bash -c 'echo | nc ${TARGET_IP} ${port}' 2>/dev/null | head -1 || true;
                      echo ''; echo '=== NMAP SSH SCRIPTS ===';
                      nmap --script ssh2-enum-algos,ssh-hostkey -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/ssh_${port}.txt' 2>&1"
                ;;
            25)
                run_parallel "SMTP_enum_${port}" bash -c "
                    { echo '=== SMTP ENUM ===';
                      command -v smtp-user-enum &>/dev/null && smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t ${TARGET_IP} -p ${port} 2>/dev/null || true;
                      nmap --script smtp-enum-users,smtp-open-relay,smtp-commands -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/smtp_${port}.txt' 2>&1"
                ;;
            53)
                run_parallel "DNS_enum_${port}" bash -c "
                    { echo '=== ZONE TRANSFER ===';
                      dig axfr @${TARGET_IP} ${TARGET_DOMAIN} 2>/dev/null || true;
                      nmap --script dns-zone-transfer,dns-recursion -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/dns_${port}.txt' 2>&1"
                ;;
            80|443|8080|8443|8000|8888)
                run_parallel "HTTP_scripts_${port}" bash -c "
                    nmap --script http-headers,http-methods,http-title,http-server-header,http-robots.txt,http-enum -p ${port} ${TARGET_IP} > '${out_base}/http_scripts_${port}.txt' 2>&1 || true"
                ;;
            111)
                run_parallel "RPC_enum_${port}" bash -c "
                    { rpcinfo -p ${TARGET_IP} 2>/dev/null || true;
                      nmap --script rpcinfo -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/rpc_${port}.txt' 2>&1"
                ;;
            139|445)
                run_parallel "SMB_enum_${port}" bash -c "
                    { echo '=== NBTSCAN ==='; nbtscan ${TARGET_IP} 2>/dev/null || true;
                      echo ''; echo '=== ENUM4LINUX ==='; enum4linux -a ${TARGET_IP} 2>/dev/null || true;
                      echo ''; echo '=== SMBCLIENT NULL ==='; smbclient -L //${TARGET_IP} -N 2>/dev/null || true;
                      echo ''; echo '=== NMAP SMB ==='; nmap --script smb-enum-shares,smb-enum-users,smb-os-discovery,smb-security-mode -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/smb_${port}.txt' 2>&1"
                ;;
            161)
                run_parallel "SNMP_enum_${port}" bash -c "
                    { snmpwalk -c public -v2c ${TARGET_IP} 2>/dev/null | head -200 || true;
                      nmap --script snmp-info,snmp-interfaces,snmp-sysdescr -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/snmp_${port}.txt' 2>&1"
                ;;
            389|636)
                run_parallel "LDAP_enum_${port}" bash -c "
                    nmap --script ldap-search,ldap-rootdse -p ${port} ${TARGET_IP} > '${out_base}/ldap_${port}.txt' 2>&1 || true"
                ;;
            2049)
                run_parallel "NFS_enum_${port}" bash -c "
                    { showmount -e ${TARGET_IP} 2>/dev/null || true;
                      nmap --script nfs-showmount,nfs-ls -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/nfs_${port}.txt' 2>&1"
                ;;
            3306)
                run_parallel "MySQL_enum_${port}" bash -c "
                    nmap --script mysql-info,mysql-empty-password -p ${port} ${TARGET_IP} > '${out_base}/mysql_${port}.txt' 2>&1 || true"
                ;;
            5432)
                run_parallel "PgSQL_enum_${port}" bash -c "
                    nmap --script pgsql-info -p ${port} ${TARGET_IP} > '${out_base}/pgsql_${port}.txt' 2>&1 || true"
                ;;
            6379)
                run_parallel "Redis_enum_${port}" bash -c "
                    { timeout 5 redis-cli -h ${TARGET_IP} -p ${port} INFO 2>/dev/null || echo 'Auth required or refused';
                      nmap --script redis-info -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/redis_${port}.txt' 2>&1"
                ;;
            3389)
                run_parallel "RDP_enum_${port}" bash -c "
                    nmap --script rdp-enum-encryption -p ${port} ${TARGET_IP} > '${out_base}/rdp_${port}.txt' 2>&1 || true"
                ;;
            *)
                run_parallel "Generic_enum_${port}" bash -c "
                    { echo '=== BANNER ===';
                      timeout 5 bash -c 'echo | nc ${TARGET_IP} ${port}' 2>/dev/null | head -5 || true;
                      echo ''; echo '=== NMAP -sC ===';
                      nmap -sC -p ${port} ${TARGET_IP} 2>/dev/null || true;
                    } > '${out_base}/generic_${port}.txt' 2>&1"
                ;;
        esac
    done

    wait_all_jobs
    update_phase "port_services" "done"
    log_success "Port-specific enumeration complete: ${out_base}/"
}

#--- Phase 7: Advanced Web Scans -----------------------------------------------
run_advanced_web() {
    # Nikto
    if should_run_phase "nikto"; then
        update_phase "nikto" "running"
        log_phase "NIKTO (Parallel)"
        if command_exists nikto; then
            for port in "${HTTP_PORTS[@]}"; do
                NIKTO_OUTPUT_FILE="${SCAN_BASE_DIR}/nikto/nikto_${TARGET_IP}_p${port}_$(timestamp).txt"
                run_parallel "nikto_http_${port}" \
                    nikto -h "http://${TARGET_IP}:${port}" -o "$NIKTO_OUTPUT_FILE" -timeout 10 -maxtime 300
            done
            wait_all_jobs
            update_phase "nikto" "done"
        else
            log_warn "nikto not available"
            update_phase "nikto" "skipped"
        fi
    fi

    # WPScan
    if should_run_phase "wpscan"; then
        update_phase "wpscan" "running"
        log_phase "WPSCAN (Parallel)"
        if command_exists wpscan; then
            for port in "${HTTP_PORTS[@]}"; do
                WPSCAN_OUTPUT_FILE="${SCAN_BASE_DIR}/wpscan/wpscan_${TARGET_IP}_p${port}_$(timestamp).txt"
                run_parallel "wpscan_http_${port}" \
                    wpscan --url "http://${TARGET_IP}:${port}" --output "$WPSCAN_OUTPUT_FILE" --disable-tls-checks --enumerate u,p,t
            done
            wait_all_jobs
            update_phase "wpscan" "done"
        else
            log_warn "wpscan not available"
            update_phase "wpscan" "skipped"
        fi
    fi

    # Dirsearch
    if should_run_phase "dirsearch"; then
        update_phase "dirsearch" "running"
        log_phase "DIRSEARCH (Parallel)"
        # FIX: Verify dirsearch actually works before launching
        if command_exists dirsearch && dirsearch --version &>/dev/null; then
            local ds_wl="${WL_DIR_BIG:-$WL_DIR_MEDIUM}"
            for port in "${HTTP_PORTS[@]}"; do
                DIRSEARCH_OUTPUT_FILE="${SCAN_BASE_DIR}/dirsearch/dirsearch_${TARGET_IP}_p${port}_$(timestamp).txt"
                run_parallel "dirsearch_http_${port}" \
                    dirsearch -u "http://${TARGET_IP}:${port}/" -o "$DIRSEARCH_OUTPUT_FILE" \
                        --format=plain -t "$GOBUSTER_THREADS" -x 404,403 -w "$ds_wl"
            done
            wait_all_jobs
            update_phase "dirsearch" "done"
        else
            log_warn "dirsearch not available or broken (see earlier Python warning)"
            update_phase "dirsearch" "skipped"
        fi
    fi
}

#--- Phase 8: Reports ----------------------------------------------------------
generate_report_markdown() {
    local report_file="${SCAN_BASE_DIR}/Reports/report_${TARGET_IP}_$(timestamp).md"
    {
        echo "# EasyScan v${SCRIPT_VERSION} Report"
        echo ""
        echo "| Field | Value |"
        echo "|-------|-------|"
        echo "| **Target IP** | ${TARGET_IP} |"
        echo "| **Domain** | ${TARGET_DOMAIN:-N/A} |"
        echo "| **Scan Date** | $(date '+%Y-%m-%d %H:%M:%S %Z') |"
        echo "| **Scan ID** | ${SCAN_ID} |"
        echo ""
        echo "---"
        echo ""
        echo "## Nmap Scan Results"
        echo '```'
        if [[ -f "${NMAP_OUTPUT_FILE:-}" ]]; then
            local pl sl
            pl=$(grep -n "^PORT\|^# Ports" "$NMAP_OUTPUT_FILE" | head -1 | cut -d: -f1)
            sl=$(grep -n "^Service Info\|# Service\|^# Nmap done" "$NMAP_OUTPUT_FILE" | head -1 | cut -d: -f1)
            if [[ -n "$pl" ]]; then
                if [[ -n "$sl" ]]; then sed -n "${pl},${sl}p" "$NMAP_OUTPUT_FILE" | grep -v "^SF:"
                else sed -n "${pl},$((pl+30))p" "$NMAP_OUTPUT_FILE" | grep -v "^SF:"; fi
            else cat "$NMAP_OUTPUT_FILE"; fi
        else echo "[No nmap data]"; fi
        echo '```'
        echo ""
        echo "## Directory / DNS / VHost (Gobuster)"
        echo '```'
        [[ -s "${GOBUSTER_OUTPUT_FILE:-}" ]] && cat "$GOBUSTER_OUTPUT_FILE" || echo "[No gobuster findings]"
        echo '```'
        echo ""
        echo "## Recursive Fuzzing (FFuF)"
        echo '```'
        [[ -s "${FFUF_OUTPUT_FILE:-}" ]] && cat "$FFUF_OUTPUT_FILE" || echo "[No ffuf findings]"
        echo '```'
        echo ""
        echo "## Port-Specific Service Enumeration"
        local svc_dir="${SCAN_BASE_DIR}/port_services/${TARGET_IP}"
        if [[ -d "$svc_dir" ]] && ls "$svc_dir"/*.txt &>/dev/null; then
            for f in "$svc_dir"/*.txt; do
                echo "### $(basename "$f" .txt)"
                echo '```'
                head -100 "$f"
                echo '```'
                echo ""
            done
        else echo "[No port-specific data]"; echo ""; fi
        [[ -s "${NIKTO_OUTPUT_FILE:-}" ]] && { echo "## Nikto"; echo '```'; cat "$NIKTO_OUTPUT_FILE"; echo '```'; echo ""; }
        [[ -s "${WPSCAN_OUTPUT_FILE:-}" ]] && { echo "## WPScan"; echo '```'; cat "$WPSCAN_OUTPUT_FILE"; echo '```'; echo ""; }
        [[ -s "${DIRSEARCH_OUTPUT_FILE:-}" ]] && { echo "## Dirsearch"; echo '```'; cat "$DIRSEARCH_OUTPUT_FILE"; echo '```'; echo ""; }
        echo "## Screenshots (Gowitness)"
        if [[ -d "${GOWITNESS_DIR:-}" ]] && ls "$GOWITNESS_DIR"/*.png &>/dev/null; then
            for img in "$GOWITNESS_DIR"/*.png; do echo "- $(basename "$img")"; done
        else echo "[No screenshots]"; fi
        echo ""
        echo "---"
        echo "*Generated by EasyScan v${SCRIPT_VERSION} on $(date)*"
    } > "$report_file"
    REPORT_FILE="$report_file"
    log_success "Markdown report: $report_file"
}

generate_report_html() {
    local report_file="${SCAN_BASE_DIR}/Reports/report_${TARGET_IP}_$(timestamp).html"
    {
        cat << 'HTMLHEAD'
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>EasyScan Report</title>
<style>
:root{--bg:#1a1a2e;--card:#16213e;--accent:#0f3460;--text:#e0e0e0;--green:#4caf50;--yellow:#ff9800;--blue:#2196f3}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'JetBrains Mono',monospace;background:var(--bg);color:var(--text);padding:2rem;line-height:1.6}
h1{color:var(--blue);border-bottom:2px solid var(--accent);padding-bottom:.5rem;margin-bottom:1rem}
h2{color:var(--green);margin:2rem 0 1rem;border-left:4px solid var(--green);padding-left:.75rem}
h3{color:var(--yellow);margin:1rem 0 .5rem}
table{width:100%;border-collapse:collapse;margin:1rem 0}
th,td{padding:.5rem 1rem;border:1px solid var(--accent);text-align:left}
th{background:var(--accent);color:#fff}
pre{background:var(--card);padding:1rem;border-radius:6px;overflow-x:auto;margin:.5rem 0;font-size:.85rem}
img.ss{max-width:100%;border:1px solid var(--accent);border-radius:6px;margin:.5rem 0}
</style></head><body>
HTMLHEAD
        echo "<h1>EasyScan v${SCRIPT_VERSION} Report</h1>"
        echo "<table><tr><th>Field</th><th>Value</th></tr>"
        echo "<tr><td>Target</td><td>${TARGET_IP}</td></tr>"
        echo "<tr><td>Domain</td><td>${TARGET_DOMAIN:-N/A}</td></tr>"
        echo "<tr><td>Date</td><td>$(date '+%Y-%m-%d %H:%M:%S %Z')</td></tr></table>"

        html_escape() { sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g'; }

        echo "<h2>Nmap</h2><pre>"
        [[ -f "${NMAP_OUTPUT_FILE:-}" ]] && html_escape < "$NMAP_OUTPUT_FILE" | head -80 || echo "[No data]"
        echo "</pre>"

        echo "<h2>Gobuster</h2><pre>"
        [[ -s "${GOBUSTER_OUTPUT_FILE:-}" ]] && html_escape < "$GOBUSTER_OUTPUT_FILE" || echo "[No findings]"
        echo "</pre>"

        echo "<h2>FFuF</h2><pre>"
        [[ -s "${FFUF_OUTPUT_FILE:-}" ]] && html_escape < "$FFUF_OUTPUT_FILE" || echo "[No findings]"
        echo "</pre>"

        echo "<h2>Port Services</h2>"
        local svc_dir="${SCAN_BASE_DIR}/port_services/${TARGET_IP}"
        if [[ -d "$svc_dir" ]] && ls "$svc_dir"/*.txt &>/dev/null; then
            for f in "$svc_dir"/*.txt; do
                echo "<h3>$(basename "$f" .txt)</h3><pre>"
                html_escape < "$f" | head -100
                echo "</pre>"
            done
        fi

        [[ -s "${NIKTO_OUTPUT_FILE:-}" ]] && { echo "<h2>Nikto</h2><pre>"; html_escape < "$NIKTO_OUTPUT_FILE"; echo "</pre>"; }
        [[ -s "${WPSCAN_OUTPUT_FILE:-}" ]] && { echo "<h2>WPScan</h2><pre>"; html_escape < "$WPSCAN_OUTPUT_FILE"; echo "</pre>"; }
        [[ -s "${DIRSEARCH_OUTPUT_FILE:-}" ]] && { echo "<h2>Dirsearch</h2><pre>"; html_escape < "$DIRSEARCH_OUTPUT_FILE"; echo "</pre>"; }

        echo "<h2>Screenshots</h2>"
        if [[ -d "${GOWITNESS_DIR:-}" ]] && ls "$GOWITNESS_DIR"/*.png &>/dev/null; then
            for img in "$GOWITNESS_DIR"/*.png; do echo "<img class='ss' src='file://$(realpath "$img")'>"; done
        else echo "<p>[None]</p>"; fi

        echo "<hr><p><em>EasyScan v${SCRIPT_VERSION} — $(date)</em></p></body></html>"
    } > "$report_file"
    REPORT_FILE="$report_file"
    log_success "HTML report: $report_file"
}

generate_report() {
    should_run_phase "report" || return 0
    update_phase "report" "running"
    log_phase "GENERATING REPORT (${REPORT_FORMAT})"
    case "$REPORT_FORMAT" in
        html) generate_report_html ;;
        *)    generate_report_markdown ;;
    esac
    update_phase "report" "done"
    update_state_field "completed_at" "$(date -Iseconds)"
}

#--- Cleanup -------------------------------------------------------------------
cleanup_all() {
    kill_all_jobs
    [[ -n "${STATE_FILE:-}" && -f "${STATE_FILE:-}" ]] && log_info "State preserved: $STATE_FILE"
}
trap 'echo ""; log_warn "Interrupted."; cleanup_all; exit 130' SIGINT SIGTERM

#--- Main ----------------------------------------------------------------------
main() {
    show_banner
    check_tools

    # FIX: Detect wordlists BEFORE asking for target, so we can die early
    detect_wordlists

    log_header "Report Format"
    echo "  1) Markdown (.md)"
    echo "  2) HTML (.html)"
    prompt_read "Select [1/2]: " fmt_choice
    case "$fmt_choice" in 2) REPORT_FORMAT="html" ;; *) REPORT_FORMAT="markdown" ;; esac

    log_header "Target Configuration"
    prompt_read "Target IP: " TARGET_IP
    validate_ip "$TARGET_IP" || die "Invalid IP: $TARGET_IP"
    prompt_read "Domain (or 'skip'): " TARGET_DOMAIN
    [[ "$TARGET_DOMAIN" == "skip" ]] && TARGET_DOMAIN=""

    setup_directories
    [[ -n "$TARGET_DOMAIN" ]] && add_to_hosts
    init_state

    prompt_read "Begin scan? [yes/no]: " go
    [[ "$go" != "yes" ]] && { log_info "Aborted."; exit 0; }

    run_nmap
    extract_ports

    (( ${#HTTP_PORTS[@]} == 0 && ${#HTTPS_PORTS[@]} == 0 )) && \
        log_warn "No web ports. Web scans will be skipped."

    (( ${#HTTP_PORTS[@]} > 0 || ${#HTTPS_PORTS[@]} > 0 )) && run_gobuster
    (( ${#HTTP_PORTS[@]} > 0 || ${#HTTPS_PORTS[@]} > 0 )) && run_ffuf
    (( ${#HTTP_PORTS[@]} > 0 || ${#HTTPS_PORTS[@]} > 0 )) && run_gowitness
    (( ${#ALL_OPEN_PORTS[@]} > 0 )) && run_port_services
    (( ${#HTTP_PORTS[@]} > 0 )) && run_advanced_web

    generate_report

    log_header "SCAN COMPLETE"
    log_info "Scan ID:    ${SCAN_ID}"
    log_info "Report:     ${REPORT_FILE}"
    log_info "State:      ${STATE_FILE}"
    log_info "Job logs:   ${SCAN_BASE_DIR}/.joblogs/"
    echo ""

    if [[ "$REPORT_FORMAT" == "html" ]]; then
        prompt_read "Open in browser? [yes/no]: " oc
        [[ "$oc" == "yes" ]] && xdg-open "$REPORT_FILE" 2>/dev/null || true
    else
        head -60 "$REPORT_FILE"
        echo -e "\n${DIM}... (see full file)${NC}"
    fi

    echo ""
    log_success "Done. Happy hacking, Boss."
}

main "$@"
