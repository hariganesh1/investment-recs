from openai import AzureOpenAI

def get_sentiment(ticker, text):
    # Setup
    endp = " YOUR ENDPOIT "
    api_key = " YOUR API KEY "
    deployment_name = " YOUR DEPLOYMENT NAME "

    prompt = f"""
    Identify the sentiment towards {ticker} on a scale of -10 (most negative sentiment) to 10 (most positive), with 0 being neutral.

    Text: {text}
    """
    
    # Create client
    client = AzureOpenAI(
        azure_endpoint = endp, 
        api_key=api_key,  
        api_version="2024-02-01"
    )
    
    # Get response
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    # Get sentiment
    sentiment = response.choices[0].message.content # It's a string yup
    return sentiment
