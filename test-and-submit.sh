#!/bin/bash

# test-and-submit.sh
# Script to submit year solutions to the quantmas automation endpoint
# Usage: ./test-and-submit.sh <year_no>

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Function to show usage
show_usage() {
    echo "Usage: $0 <year_no>"
    echo ""
    echo "Arguments:"
    echo "  year_no    The year number (e.g., 1, 2, 3, etc.)"
    echo ""
    echo "Examples:"
    echo "  $0 1       Submit year 1 solution"
    echo "  $0 2       Submit year 2 solution"
    echo ""
    echo "Requirements:"
    echo "  - .env file must contain DEVHUB_TOKEN"
    echo "  - submissions/year_<year_no>/output/output.yml must exist"
}

# Check if year_no argument is provided
if [ $# -eq 0 ] || [ -z "$1" ]; then
    print_error "Year number argument is required"
    show_usage
    exit 1
fi

YEAR_NO="$1"

# Validate year_no is a number
if ! [[ "$YEAR_NO" =~ ^[0-9]+$ ]]; then
    print_error "Year number must be a positive integer"
    show_usage
    exit 1
fi

print_info "Starting submission process for Year $YEAR_NO"

# Function to get token from user
get_token_from_user() {
    local is_retry="$1"
    
    if [ "$is_retry" = "true" ]; then
        print_warning "Previous token was invalid or expired"
    fi
    
    print_info "Opening browser to get DEVHUB_TOKEN..."
    
    # Open browser to token page
    if command -v open > /dev/null 2>&1; then
        # macOS
        open "http://xxx/quantmas/token"
    elif command -v xdg-open > /dev/null 2>&1; then
        # Linux
        xdg-open "http://xxx/quantmas/token"
    elif command -v start > /dev/null 2>&1; then
        # Windows (Git Bash, etc.)
        start "http://xxx/quantmas/token"
    else
        print_warning "Could not open browser automatically"
        print_info "Please manually open: http://xxx/quantmas/token"
    fi
    
    print_info "Please copy the token from the browser and paste it here:"
    echo -n "Token: "
    read -r USER_TOKEN
    
    if [ -z "$USER_TOKEN" ]; then
        print_error "No token entered"
        exit 1
    fi
    
    # Update or create .env file
    if [ -f ".env" ]; then
        # Remove existing DEVHUB_TOKEN line and add new one
        grep -v "^DEVHUB_TOKEN=" .env > .env.tmp 2>/dev/null || touch .env.tmp
        echo "DEVHUB_TOKEN=$USER_TOKEN" >> .env.tmp
        mv .env.tmp .env
    else
        echo "DEVHUB_TOKEN=$USER_TOKEN" > .env
    fi
    
    # Set the token for current session
    DEVHUB_TOKEN="$USER_TOKEN"
    
    print_success "Token saved to .env file"
}

# Function to clear token from .env
clear_token() {
    if [ -f ".env" ]; then
        grep -v "^DEVHUB_TOKEN=" .env > .env.tmp 2>/dev/null || touch .env.tmp
        mv .env.tmp .env
        print_info "Token cleared from .env file"
    fi
    unset DEVHUB_TOKEN
}

# Step 1: Check if .env file exists and contains DEVHUB_TOKEN
print_info "Checking for .env file and DEVHUB_TOKEN..."

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    touch .env
    print_info "Created .env file"
fi

# Source the .env file
source .env

# Step 2: Get token if not present
if [ -z "$DEVHUB_TOKEN" ]; then
    print_warning "DEVHUB_TOKEN not found in .env file"
    get_token_from_user false
else
    print_success "DEVHUB_TOKEN found in .env file"
fi

# Step 3: Check if output.yml file exists
OUTPUT_FILE="submissions/year_${YEAR_NO}/output/output.yml"
print_info "Checking for output file: $OUTPUT_FILE"

if [ ! -f "$OUTPUT_FILE" ]; then
    print_error "Output file not found: $OUTPUT_FILE"
    print_info "Expected file structure: submissions/year_${YEAR_NO}/output/output.yml"
    exit 1
fi

print_success "Output file found: $OUTPUT_FILE"

# Step 4: Read the output.yml file and validate it's not empty
print_info "Reading output data from $OUTPUT_FILE"

if [ ! -s "$OUTPUT_FILE" ]; then
    print_error "Output file is empty: $OUTPUT_FILE"
    exit 1
fi

# Read the YAML content
OUTPUT_DATA=$(cat "$OUTPUT_FILE")

# Basic YAML validation (check if file starts with valid YAML)
if ! echo "$OUTPUT_DATA" | head -1 | grep -qE '^[a-zA-Z0-9_-]+:' && ! echo "$OUTPUT_DATA" | head -1 | grep -q '^---'; then
    print_warning "Output file might not be valid YAML format"
fi

print_success "Output data loaded successfully ($(wc -l < "$OUTPUT_FILE") lines)"

# Step 5: Prepare JSON payload
print_info "Preparing submission payload..."

# Create a temporary file for the JSON payload
TEMP_JSON=$(mktemp)
trap "rm -f $TEMP_JSON" EXIT

# Convert YAML to JSON-compatible format and create payload
# We'll embed the YAML content as a string in the JSON
cat << EOF > "$TEMP_JSON"
{
  "year": $YEAR_NO,
  "data": $(echo "$OUTPUT_DATA" | jq -Rs .)
}
EOF

print_success "Payload prepared successfully"

# Step 6: Submit to API endpoint (with retry logic for unauthorized)
API_ENDPOINT="http://xxx/workflows/automation/quantmas"
MAX_RETRIES=2
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    print_info "Submitting to: $API_ENDPOINT (Attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)"

    # Make the POST request
    print_info "Making API request..."

    HTTP_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}\nHTTP_SIZE:%{size_download}" \
      -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $DEVHUB_TOKEN" \
      -d "@$TEMP_JSON" \
      "$API_ENDPOINT")

    # Parse the response
    HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed -E 's/HTTP_STATUS:[0-9]+.*$//')
    HTTP_STATUS=$(echo "$HTTP_RESPONSE" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
    RESPONSE_SIZE=$(echo "$HTTP_RESPONSE" | grep -o "HTTP_SIZE:[0-9]*" | cut -d: -f2)

    print_info "Response received (Status: $HTTP_STATUS, Size: ${RESPONSE_SIZE} bytes)"

    # Check if unauthorized
    if [ "$HTTP_STATUS" = "401" ]; then
        print_error "Unauthorized (HTTP 401) - Token is invalid or expired"
        
        if [ $RETRY_COUNT -lt $((MAX_RETRIES - 1)) ]; then
            print_info "Clearing token and requesting new one..."
            clear_token
            get_token_from_user true
            RETRY_COUNT=$((RETRY_COUNT + 1))
        else
            print_error "Maximum retry attempts reached. Exiting."
            echo ""
            echo "Response details:"
            echo "$HTTP_BODY"
            exit 1
        fi
    else
        # Break out of retry loop for any other status
        break
    fi
done

# Step 7: Render the response
print_info "API Response:"
echo "============================================"

if [ "$HTTP_STATUS" -ge 200 ] && [ "$HTTP_STATUS" -lt 300 ]; then
    print_success "Submission successful (HTTP $HTTP_STATUS)"
    echo ""
    
    # Try to pretty-print JSON if possible
    if echo "$HTTP_BODY" | jq . > /dev/null 2>&1; then
        echo "$HTTP_BODY" | jq .
    else
        echo "$HTTP_BODY"
    fi
    
elif [ "$HTTP_STATUS" -ge 400 ] && [ "$HTTP_STATUS" -lt 500 ]; then
    print_error "Client error (HTTP $HTTP_STATUS)"
    echo ""
    echo "$HTTP_BODY"
    exit 1
    
elif [ "$HTTP_STATUS" -ge 500 ]; then
    print_error "Server error (HTTP $HTTP_STATUS)"
    echo ""
    echo "$HTTP_BODY"
    exit 1
    
else
    print_warning "Unexpected response (HTTP $HTTP_STATUS)"
    echo ""
    echo "$HTTP_BODY"
fi

echo "============================================"
print_success "Submission process completed for Year $YEAR_NO"

# Optional: Log the submission
LOG_DIR=".agent_log"
LOG_FILE="$LOG_DIR/$(date +%Y).log"

mkdir -p "$LOG_DIR"

cat << EOF >> "$LOG_FILE"
[$(date '+%Y-%m-%d %H:%M:%S')] SUBMISSION
Year: $YEAR_NO
Status: HTTP $HTTP_STATUS
Output File: $OUTPUT_FILE
Response Size: ${RESPONSE_SIZE} bytes
---
EOF

print_info "Submission logged to: $LOG_FILE"