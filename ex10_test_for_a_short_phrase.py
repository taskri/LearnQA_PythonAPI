class TestShortPhrase:
    def test_short_phrase(self):
        phrase = input("Set a phrase:")
        assert len(phrase) < 15, "Phrase consists of 15 symbols or more"
