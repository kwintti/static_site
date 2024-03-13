from textnode import TextNode

def main():
    site = TextNode("kokeilu", "bold", "www.google.com")
    site.url = "www.google.com"
    print(site)

main()

