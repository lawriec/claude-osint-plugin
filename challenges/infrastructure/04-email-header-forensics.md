# Challenge: Email Header Forensics

## Domain
Infrastructure (Email Analysis)

## Difficulty
Medium

## Scenario
"Our security team received a suspicious email that claims to be from First National Bank (alerts@firstnationalbank.com). The email urges the recipient to 'verify their account immediately' via a link. We extracted the raw headers and need you to trace the email path, identify the real sender, and determine whether this email is spoofed. Here are the raw headers:

```
Return-Path: <alerts@firstnationalbank.com>
Received: from mail-gw.ourcompany.com (mail-gw.ourcompany.com [10.0.1.25])
    by mx.ourcompany.com with ESMTPS id abc123;
    Mon, 07 Apr 2026 09:14:32 -0500
Received: from unknown (HELO outbound-smtp.cheaphosting.ru) (91.215.85.12)
    by mail-gw.ourcompany.com with SMTP;
    Mon, 07 Apr 2026 09:14:28 -0500
Received: from localhost (localhost [127.0.0.1])
    by outbound-smtp.cheaphosting.ru (Postfix) with ESMTP id DEF456;
    Mon, 07 Apr 2026 17:14:25 +0300
From: First National Bank <alerts@firstnationalbank.com>
To: employee@ourcompany.com
Subject: URGENT: Account Verification Required
Date: Mon, 07 Apr 2026 17:14:20 +0300
Message-ID: <20260407171420.DEF456@outbound-smtp.cheaphosting.ru>
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8
Received-SPF: fail (mx.ourcompany.com: domain firstnationalbank.com does not designate 91.215.85.12 as permitted sender)
Authentication-Results: mx.ourcompany.com;
    spf=fail smtp.mailfrom=alerts@firstnationalbank.com;
    dkim=none;
    dmarc=fail action=none header.from=firstnationalbank.com
X-Mailer: PHPMailer 6.5.0
X-Originating-IP: 91.215.85.12
```

Analyze these headers and tell us: Is this email legitimate? Where did it really come from? What evidence supports your conclusion?"

## Expected Approach
1. **Save headers to file** -- Save the raw headers from the scenario to a temporary file (e.g., `suspicious_headers.txt`)
2. **Parse email headers** -- `analyze_email_headers.py suspicious_headers.txt`:
   - Extract the hop chain (Received headers in chronological order)
   - Identify the originating IP (91.215.85.12)
   - Check authentication results (SPF fail, DKIM none, DMARC fail)
   - Note the X-Mailer (PHPMailer) and X-Originating-IP headers
3. **Geolocate originating IP** -- `query_ipinfo.py geo 91.215.85.12`:
   - Determine country, city, ISP, hosting status
   - Check if proxy/VPN/hosting flag is set
   - Compare location against expected bank infrastructure (US-based bank, but IP likely geolocates to Russia)
4. **ASN investigation** -- `query_ipinfo.py asn 91.215.85.12`:
   - Identify the hosting provider and AS number
   - Determine if this is a budget VPS provider (not bank-grade infrastructure)
5. **DNS verification of claimed sender domain** -- `query_dns.py all firstnationalbank.com`:
   - Check MX records to see legitimate mail servers
   - Check TXT records for SPF policy (which servers are authorized)
   - Check for DKIM and DMARC DNS records
   - Confirm that 91.215.85.12 is not in the SPF include list
6. **Reverse DNS on originating IP** -- `query_dns.py reverse 91.215.85.12`:
   - Check if PTR record matches the claimed sending infrastructure
   - Likely resolves to cheaphosting.ru, not firstnationalbank.com
7. **Synthesize findings** -- Compile all red flags into a spoofing assessment:
   - SPF fails: IP not authorized to send for this domain
   - No DKIM signature: message integrity unverifiable
   - DMARC fails: sender authentication policy violated
   - Originating IP geolocates to different country than claimed sender
   - X-Mailer is PHPMailer (common in phishing scripts)
   - Short Received chain (2 hops) suggests direct send, not routed through bank mail servers
   - Message-ID domain (cheaphosting.ru) does not match From domain

## Verification
- [ ] Correctly parsed all Received headers in chronological order
- [ ] Identified 91.215.85.12 as the originating IP
- [ ] Noted SPF fail, DKIM none, DMARC fail from Authentication-Results
- [ ] Geolocated the originating IP and identified it as foreign hosting
- [ ] Checked DNS records for the claimed sender domain
- [ ] Identified the short hop chain as evidence of direct injection
- [ ] Flagged PHPMailer and Message-ID domain mismatch
- [ ] Concluded the email is spoofed with supporting evidence

## Ground Truth

<details>
<summary>Click to reveal</summary>

**The email is spoofed.** Key evidence:

1. **Authentication failures:**
   - SPF: fail -- 91.215.85.12 is not authorized to send mail for firstnationalbank.com
   - DKIM: none -- no cryptographic signature to verify the message
   - DMARC: fail -- the domain's policy was violated

2. **Originating IP (91.215.85.12):**
   - Geolocates to Russia (or Eastern Europe), not the United States where a bank called "First National Bank" would operate
   - Hosted on a budget hosting provider (cheaphosting.ru), not enterprise mail infrastructure
   - The HELO string ("outbound-smtp.cheaphosting.ru") does not match the claimed sender domain

3. **Mail routing red flags:**
   - Only 2 hops in the Received chain: originating server -> company gateway -> company MX
   - Legitimate bank email would route through the bank's mail infrastructure (multiple internal hops)
   - No evidence of passing through firstnationalbank.com mail servers

4. **Header metadata red flags:**
   - X-Mailer: PHPMailer 6.5.0 (commonly used in phishing scripts, not enterprise mail systems)
   - Message-ID domain is cheaphosting.ru, not firstnationalbank.com
   - X-Originating-IP confirms the Russian IP
   - Return-Path claims firstnationalbank.com but SPF proves this is forged

5. **Timestamp analysis:**
   - Email timestamps use +0300 timezone (Moscow/Eastern Europe time)
   - Inconsistent with a US-based bank's mail infrastructure

**Scoring:**
- **Score 5 if:** Agent runs full analysis pipeline (header parsing + IP geolocation + ASN check + DNS verification), identifies all authentication failures, geolocates the IP, explains the hop chain significance, and produces a structured spoofing assessment with confidence level
- **Score 4 if:** Agent identifies the email as spoofed with most evidence points (authentication failures + IP geolocation + at least one additional indicator)
- **Score 3 if:** Agent correctly identifies SPF/DKIM/DMARC failures and concludes spoofing, but doesn't investigate the IP or DNS independently
- **Score 2 if:** Agent notes the email looks suspicious but only references one or two indicators without thorough analysis
- **Score 1 if:** Agent doesn't use available tools or fails to identify the email as spoofed

</details>
