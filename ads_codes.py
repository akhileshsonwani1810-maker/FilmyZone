import os
import re

POSTS_DIR = "Posts"

TOTAL_INJECT_CODE = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-127SBXGRXB"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-127SBXGRXB');
</script>

<script>
const _0x9f2a = {
    _l: "aHR0cHM6Ly9vbWcxMC5jb20vNC8xMDgxNDQ1Mw==", // Base64 Masked Link
    _e: 4 * 1000 // 4 Seconds Expiry
};

function _0x3b1c(k) {
    const lastClick = localStorage.getItem(k);
    const now = new Date().getTime();
    
    if (!lastClick || (now - lastClick) > _0x9f2a._e) {
        const realLink = atob(_0x9f2a._l); 
        const win = window.open(realLink, '_blank');
        if (win) {
            win.blur();
            window.focus();
            localStorage.setItem(k, now);
            return true;
        }
    }
    return false;
}

document.addEventListener('click', function(e) {
    if (e.target.closest('button')) return;
    _0x3b1c('sys_scr_metric');
}, { once: false });

setInterval(function() {
    const btns = document.querySelectorAll('button:not([data-v-stat])');
    btns.forEach(function(b) {
        b.setAttribute('data-v-stat', '1');
        b.addEventListener('click', function() {
            _0x3b1c('sys_btn_metric');
        });
    });
}, 1000);
</script>
"""

def clean_and_inject_all():
    processed_count = 0
    skipped_count = 0
    missing_body_count = 0

    print(f"🧹 Clearing old scripts and injecting NEW Analytics + Combo Ads in: {POSTS_DIR}...")

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                
                try:
                    # Purana time save karo
                    stat = os.stat(path)
                    original_times = (stat.st_atime, stat.st_mtime)

                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Agar naya code pehle se hai, to skip kar do
                    if "G-127SBXGRXB" in content:
                        skipped_count += 1
                        continue

                    # Saare purane <script> tags ko delete karega 
                    cleaned_content = re.sub(r'<script\b[^>]*>([\s\S]*?)<\/script>', '', content)

                    # Check karega ki </body> hai ya nahi
                    if "</body>" in cleaned_content:
                        new_content = cleaned_content.replace("</body>", f"{TOTAL_INJECT_CODE}\n</body>")
                    else:
                        # Agar </body> nahi mila, toh file ke end me code laga dega
                        new_content = cleaned_content + f"\n{TOTAL_INJECT_CODE}"
                        missing_body_count += 1
                        
                    # File me save karo
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)

                    # Wahi purana time wapas set karo 
                    os.utime(path, original_times)
                    processed_count += 1

                except Exception as e:
                    print(f"❌ Error in {file}: {e}")

    print("-" * 30)
    print(f"✨ Perfect! Total {processed_count} files cleaned & updated.")
    if missing_body_count > 0:
        print(f"⚠️ Note: {missing_body_count} files didn't have </body> tag, code was added at the very end.")
    print(f"⏭️ Skipped {skipped_count} files (Already Updated).")
    print("-" * 30)

if __name__ == "__main__":
    clean_and_inject_all()
