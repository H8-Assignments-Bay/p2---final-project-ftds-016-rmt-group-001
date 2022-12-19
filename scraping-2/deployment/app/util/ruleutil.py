import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def is_subject_equal_to_symbol(row):
    """
    subject is the stock symbol discussed in the comment.
    symbol is the stock where the comment came from.
    
    Return True if subject == symbol.
    Return False if subject != symbol.
    """
    comment = row['comment']

    # Tokenisasi komentar menjadi kata-kata
    words = nltk.word_tokenize(comment)

    # Menggunakan Porter Stemmer untuk mengubah kata-kata menjadi bentuk dasar
    stemmer = nltk.PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]

    # Menggunakan part-of-speech tagging untuk mengidentifikasi jenis kata
    pos_tags = nltk.pos_tag(words)

    # Cek apakah komentar merupakan pertanyaan saham
    if 'apa' in stemmed_words or \
        'kenapa' in stemmed_words or \
        'bagaimana' in stemmed_words or \
        'gimana' in stemmed_words or \
        'kapan' in stemmed_words or \
        'dimana' in stemmed_words or \
        'siapa' in stemmed_words:
        return "Reject"

    # Cari subjek komentar
    subject = None
    for word, pos in pos_tags:
        if pos == 'NN' or pos == 'NNP':
            subject = word
            break

    # Jika tidak ada subjek komentar, maka ACCEPT
    if subject is None:
        return "Accept"

    # Cari symbol pertama dari subjek komentar
    # for symbol in symbols:
    if stemmer.stem(row['symbol']) == stemmer.stem(subject):
        return "Accept"

    # Jika tidak ditemukan symbol yang cocok, maka REJECT
    return "Reject"