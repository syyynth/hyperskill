import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from sentiment import SentimentAnalysis


def training_data(file_path: str):
    return pd.read_csv(file_path,
                       sep=',(?=[^,]*$)',
                       names=['Review', 'Score'],
                       engine='python')


def transform_data(df):
    vectorizer = TfidfVectorizer(tokenizer=SentimentAnalysis().preprocess)
    X, y = vectorizer.fit_transform(df['Review']), df['Score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    return X_train, X_test, y_train, y_test, vectorizer


def train_model(X_train, y_train):
    model = SGDClassifier()
    model.fit(X_train, y_train)

    return model


def make_predictions(model, X_test):
    return model.predict(X_test)


def sentiment_analysis(X_test, feature_names, sa):
    return [sa.classify_review([feature_names[i] for i in review.nonzero()[1]])
            for review in X_test]


def score_to_sentiment(y_scores):
    return ['Positive' if score > 5 else 'Negative' for score in y_scores]


def accuracy_report(y_real, predicted_sentiment):
    report = classification_report(y_real, predicted_sentiment, output_dict=True)
    accuracy = report['accuracy']
    worst_class = 'Positive' if (
            report['Positive']['f1-score'] < report['Negative']['f1-score']
    ) else 'Negative'

    return accuracy, worst_class


def comparison_results(rule_accuracy, sgd_accuracy, rule_worst_class, sgd_worst_class):
    better_method = 'Rule-based' if rule_accuracy > sgd_accuracy else 'SGDClassifier'
    worst_class = rule_worst_class if rule_worst_class == sgd_worst_class else 'Inconclusive'
    accuracy_difference = abs(sgd_accuracy - rule_accuracy)

    return better_method, worst_class, accuracy_difference


if __name__ == "__main__":
    sa = SentimentAnalysis()
    input_file = input()

    # Obtain training data
    df = training_data(input_file)

    # Preprocess and transform data
    X_train, X_test, y_train, y_test, vectorizer = transform_data(df)

    # Train the model
    model = train_model(X_train, y_train)

    # Make predictions
    y_pred = make_predictions(model, X_test)

    # Get feature names
    feature_names = vectorizer.get_feature_names_out()

    # Classify reviews Rule-based
    rule_sentiment = sentiment_analysis(X_test, feature_names, sa)

    # Convert scores to sentiments
    sgd_sentiment = score_to_sentiment(y_pred)
    y_real = score_to_sentiment(y_test)

    # Generate classification reports
    rule_report, rule_worst_class = accuracy_report(y_real, rule_sentiment)
    sgd_report, sgd_worst_class = accuracy_report(y_real, sgd_sentiment)

    # Compare results
    better_method, worst_class, accuracy_difference = comparison_results(rule_report,
                                                                         sgd_report,
                                                                         rule_worst_class,
                                                                         sgd_worst_class)

    print(f'The method with the better accuracy: {better_method}')
    print(f'The worst predicted class for both classifiers: {worst_class}')
    print(f'The difference between the SGDClassifier and the rule-based approach: {accuracy_difference:.2f}')
