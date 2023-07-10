from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as url

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def search():
    return render_template("index.html")


@app.route('/result', methods=["POST", "GET"])
def result():
    if request.method == "POST":
        product_name = str(request.form.get('search'))
        flipcart_url = "https://www.flipkart.com/search?q=i" + product_name
        get_response = url(flipcart_url)
        get_html = get_response.read()
        get_html_bs4 = bs(get_html, "html.parser")
        div_tag_mobile = get_html_bs4.find_all("div", {"class": "_1AtVbE col-12-12"})
        product = "https://www.flipkart.com" + div_tag_mobile[6].div.div.div.a['href']
        product6 = requests.get(product)
        product61 = bs(product6.text, "html.parser")
        product_review = product61.find_all("div", {"class": "_16PBlm"})

        reviews_list = []

        for reviews in product_review:
            try:
                person_name = reviews.div.div.find_all("p",{"class":"_2sc7ZR _2V5EHH"})[0].text
            except:
                person_name="NA"
            try:
                heading = reviews.div.div.p.text
            except:
                heading="NA"
            try:
                comment = reviews.div.div.find_all("div", {"class": "t-ZTKy"})[0].text
            except:
                comment="NA"
            try:
                date = reviews.div.div.find_all("p", {"class": "_2sc7ZR"})[1].text
            except:
                date="NA"
            try:
                rating = reviews.div.div.div.div.text
            except:
                rating="NA"
            try:
                price = reviews.find_all("div", {"class": "_30jeq3 _16Jk6d"})[0].text
            except:
                price= "NA"

            mydic = {
                # "Price":price,
                "Date":date,
                "Name": person_name,
                "Rating": rating,
                "Heading":heading,
                "Comment": comment
            }
            reviews_list.append(mydic)

        return render_template("result.html",reviews=reviews_list[0:(len(reviews_list) - 1)])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
