from django import forms


class AddSubreddit(forms.Form):
    subReddit=forms.CharField(label='Subreddit Name')