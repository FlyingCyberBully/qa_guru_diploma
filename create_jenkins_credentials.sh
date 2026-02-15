#!/bin/bash

# Jenkins credentials
JENKINS_URL="https://jenkins.autotests.cloud"
USERNAME="CyberBully"
PASSWORD="zyhvir-higkek-Haptu9"

# Get Jenkins crumb for CSRF protection
echo "Getting Jenkins crumb..."
CRUMB=$(curl -s -u "${USERNAME}:${PASSWORD}" "${JENKINS_URL}/crumbIssuer/api/json" | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['crumb'])")
CRUMB_FIELD="Jenkins-Crumb"
echo "Crumb: $CRUMB"
echo ""

# Function to create a credential
create_credential() {
    local CRED_ID="$1"
    local SECRET="$2"
    local DESCRIPTION="$3"
    
    echo "Creating credential: $CRED_ID"
    
    # Check if exists first
    CHECK_URL="${JENKINS_URL}/credentials/store/system/domain/_/credential/${CRED_ID}/"
    HTTP_CODE=$(curl -s -u "${USERNAME}:${PASSWORD}" -o /dev/null -w "%{http_code}" "$CHECK_URL")
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo "✓ SKIP: $CRED_ID - Already exists"
        echo ""
        return 0
    fi
    
    # Create JSON payload
    JSON_PAYLOAD=$(cat <<EOF
{
  "": "0",
  "credentials": {
    "scope": "GLOBAL",
    "id": "${CRED_ID}",
    "secret": "${SECRET}",
    "description": "${DESCRIPTION}",
    "\$class": "org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl"
  }
}
EOF
)
    
    # URL encode the JSON
    ENCODED_JSON=$(python3 -c "import urllib.parse; import sys; print(urllib.parse.quote(sys.argv[1]))" "$JSON_PAYLOAD")
    
    # Create the credential
    RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" \
        -u "${USERNAME}:${PASSWORD}" \
        -H "${CRUMB_FIELD}: ${CRUMB}" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        --data "json=${ENCODED_JSON}" \
        "${JENKINS_URL}/credentials/store/system/domain/_/createCredentials" 2>&1)
    
    HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | sed 's/HTTP_CODE://')
    
    if [ "$HTTP_CODE" == "200" ] || [ "$HTTP_CODE" == "302" ]; then
        echo "✓ CREATED: $CRED_ID - $DESCRIPTION"
    else
        echo "✗ FAILED: $CRED_ID - HTTP $HTTP_CODE"
        echo "$RESPONSE" | grep -v "HTTP_CODE:"
    fi
    echo ""
}

# Create all credentials
echo "============================================================"
echo "Creating Jenkins System Credentials"
echo "============================================================"
echo ""

create_credential "API_TOKEN" "***TMDB_API_TOKEN***" "TMDB API Bearer token"

create_credential "SELENOID_LOGIN" "user1" "Selenoid username"

create_credential "SELENOID_PASSWORD" "1234" "Selenoid password"

create_credential "BROWSERSTACK_USERNAME" "***BSTACK_USERNAME***" "BrowserStack username"

create_credential "BROWSERSTACK_ACCESS_KEY" "***BSTACK_ACCESS_KEY***" "BrowserStack access key"

create_credential "BROWSERSTACK_APP_URL" "***BSTACK_APP_URL***" "BrowserStack app URL"

create_credential "TG_BOT_TOKEN" "***TELEGRAM_TOKEN***" "Telegram bot token"

create_credential "TG_CHAT_ID" "534607580" "Telegram chat ID"

echo "============================================================"
echo "Credential creation complete"
echo "============================================================"
