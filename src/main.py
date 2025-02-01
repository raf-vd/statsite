from textnode import TextNode, TextType

def main():
    # print("hello world")
    # tn1a = TextNode("my first node", TextType.BOLD_TEXT)
    # tn1b = TextNode("my first node", TextType.BOLD_TEXT)
    # print(tn1)
    tn2 = TextNode("my 2nd node", TextType.LINKS, "https://www.boot.dev")
    print(tn2)
    # print(f"tn1a=tn1b: {tn1a==tn1b}")

main()
