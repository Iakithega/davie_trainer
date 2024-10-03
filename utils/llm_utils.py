

def show_result_old(result_raw):
    return result_raw["choices"][0]["message"]["content"] 

def show_result_new(result_raw):
    return result_raw.choices[0].message.content