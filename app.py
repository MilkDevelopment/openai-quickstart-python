import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_prompt(product):
    return "Write a creative ad for the following product to run on Facebook aimed at businesses:\n\nProduct:" + str(product)


def generate_proofread(proofread):
    return "Correct this to standard English:\n\n" + str(proofread)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        product = request.form["product"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(product),
            temperature=0.5,
            max_tokens=90,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/proofread", methods=("GET", "POST"))
def proofread():
    if request.method == "POST":
        proofread = request.form["text"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_proofread(proofread),
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)
