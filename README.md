# Unsplash Collection Download

Note: this is not a production-quality script, this is the start of my own
experiments with the Unsplash API. As such, it may be useful as example code,
but on its own it's only really useful to someone somewhat familiar with
Python.

Instructions for setup:

1. Create `secrets.py` defining `ACCESS_KEY` and `SECRET_KEY` as per your
   Unsplash API application keys.
1. Run `get-auth-code.py` to obtain an auth code.
1. Extract the code from the output and pass it as the sole command-line
   parameter to `get-token.py`, which will create `config.json` with the
   appropriate keys within it.
1. Update `config.json` to provide a location for `download_dir`.


