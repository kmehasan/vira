final_urls = []
with open("v2/image_db.csv", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        urls = line.split(",")
        for url in urls:
            if url.startswith("http"):
                print(url)
                if url not in final_urls:
                    final_urls.append(url)

with open("v2/image_db_final.txt", "w") as f:
    for url in final_urls:
        
        f.write(url + "\n")