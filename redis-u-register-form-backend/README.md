# TODO...

* Overview
* Python version required
* Installing functions framework locally
* Installing Python dependencies
* Example curl
* Relationship to CloudFlare rules and static site

```bash
$ functions-framework --target=register_form_processor --debug
```

Deploying Stage:

```bash
$ gcloud functions deploy stage-register-form-processor --entry-point register_form_processor --trigger-http --runtime python38 --allow-unauthenticated --env-vars-file stage_env.yaml --project redislabs-university
```

The function will then be available at:

```
https://us-central1-redislabs-university.cloudfunctions.net/stage-register-form-processor
```

Deploying Production:

```bash
$ gcloud functions deploy register-form-processor --entry-point register_form_processor --trigger-http --runtime python38 --allow-unauthenticated --env-vars-file prod_env.yaml --project redislabs-university
```

The function will then be available at:

```
https://us-central1-redislabs-university.cloudfunctions.net/register-form-processor
```