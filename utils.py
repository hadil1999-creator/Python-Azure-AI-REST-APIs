import requests as req


def call_text_analytics_api(headers, document, endpoint):
    response = req.post("https://language-project.cognitiveservices.azure.com/text/analytics/v3.1/" +
                        endpoint, headers=headers, json=document)
    return response.json()
