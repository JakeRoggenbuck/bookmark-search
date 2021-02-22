import meilisearch
import json
import shlex

client = meilisearch.Client('http://127.0.0.1:7700')


def bookmark_html_to_json():
    _id = 0
    bookmarks = []
    with open("bookmarks.html") as html_bookmarks:
        for line in html_bookmarks.readlines():
            bookmark = {}
            split_line = shlex.split(line)
            if len(split_line) > 0:
                if split_line[0] == "<DT><A":
                    line = line.strip()
                    parts = line.split(">")
                    bookmark["_id"] = _id
                    bookmark["name"] = parts[-2].rstrip("</A")
                    bookmark["url"] = parts[1].lstrip("<A HREF=").split(" ")[0][1:-1]
                    _id += 1

                    bookmarks.append(bookmark)

    with open("bookmarks.json", "w") as json_file:
        json.dump(bookmarks, json_file)


def load_bookmarks_json():
    with open('bookmarks.json') as json_file:
        bookmarks = json.load(json_file)
        client.index('bookmarks').add_documents(bookmarks)


if __name__ == "__main__":
    bookmark_html_to_json()
    load_bookmarks_json()
