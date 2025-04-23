# Opensearch SSL Issue Workaround/Possible Solution

If you are facing an SSL issue while using opensearch, you can use the following code to solve the issue.

### **Error Message Example:**
```
File."/Users/samuelcadiz/Courses/capstone/OpenSearch_Exploration/.venv/lib/python3.13/site-packages/opensearchpy/connection/http_urllib3.py", line 292, in perform_request raise SSLError ("N/A" ,
str (e), e)
opensearchpy-exceptions.SSLError: ConnectionError([SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1018)) caused by: SSLError([SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c: 1018) )
```

**Instructions:**
- Enter the create_client.py file
- Within the file head down to line 30
    - comment out the lines 34 -38
    - Add `connection_class=RequestsHttpConnection` within the parentheses of the opensearch client
        - Make sure to import RequestsHttpConnection from opensearchpy at the top of the file



### Result: This should now allow you to use opensearch without any SSL issues

NOTE: If you are still facing issues please get in touch with someone on the Data Product Team or Professor Coleman


# Some Possible Solutions Other Than The Above Mentioned

### **Resolving OpenSSL Version Mismatch on macOS**

If you're encountering OpenSSL-related errors when using **curl**, **Python**, or **OpenSearch** on macOS, it's likely due to a version mismatch. Apple ships a forked version called **LibreSSL**, which differs from the common **OpenSSL** in handling **TLS and other cryptographic functions**. OpenSearch requires **OpenSSL**, not LibreSSL.

## **Step-by-Step Fix**

### **1. Check Your Current OpenSSL Version**
Run the following commands to verify which version of OpenSSL your system is using:

```sh
which openssl
openssl version
```

If the output of `openssl version` includes **LibreSSL**, that’s likely the cause of the issue.

**Example of an incorrect version (LibreSSL from Apple):**
```sh
/usr/bin/openssl version  
LibreSSL 3.3.6  
```

---

### **2. Install OpenSSL Correctly**

#### **Option 1: Using Homebrew (Preferred)**
1. **Install OpenSSL via Homebrew:**
   ```sh
   brew install openssl
   ```
2. **Close and reopen your terminal** to apply changes.
3. **Verify that the correct OpenSSL is being used:**
   ```sh
   which openssl
   openssl version
   ```
   You should see output similar to:
   ```sh
   /opt/homebrew/bin/openssl  
   OpenSSL 3.4.0 22 Oct 2024 (Library: OpenSSL 3.4.0 22 Oct 2024)  
   ```
   If this is correct, your issue should be resolved.

#### **Option 2: Using Conda (Alternative Approach)**
If you are using Conda, you can install OpenSSL through the Conda package manager:
```sh
conda install -c conda-forge openssl
```
Then, check that the correct version is in use:
```sh
which openssl
openssl version
```
Expected output:
```sh
/Users/yourusername/miniconda3/bin/openssl  
OpenSSL 3.2.0 23 Nov 2023 (Library: OpenSSL 3.2.0 23 Nov 2023)  
```

---

### **3. Ensure OpenSSL is in Your Path**
After installation, verify that the system is correctly using the newly installed OpenSSL. The **which openssl** command should not return `/usr/bin/openssl` (which is Apple’s LibreSSL version). Instead, it should point to **Homebrew or Conda’s OpenSSL path**.

**If the issue persists:**
- Restart your terminal or machine.
- If Homebrew OpenSSL is installed but not detected, add it to your shell profile:
  ```sh
  echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
  source ~/.zshrc
  ```

---

## **Summary**
- **Problem:** macOS ships **LibreSSL**, but OpenSearch and some Python libraries require **OpenSSL**.
- **Solution:** Install OpenSSL via **Homebrew (preferred) or Conda**.
- **Verification:** Run `which openssl` and `openssl version` to confirm your system is using the correct version.

