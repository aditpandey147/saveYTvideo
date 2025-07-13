import browser_cookie3

output_path = "cookies.txt"

with open(output_path, "w") as f:
    cj = browser_cookie3.chrome(domain_name='youtube.com')
    for cookie in cj:
        f.write(f"{cookie.domain}\tTRUE\t{cookie.path}\t"
                f"{str(cookie.secure).upper()}\t{int(cookie.expires)}\t"
                f"{cookie.name}\t{cookie.value}\n")

print(f"✅ Saved cookies to {output_path}")
