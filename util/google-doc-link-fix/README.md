# google-doc-link-fix

## Purpose

This is a small utility that fixes an annoying problem with exporting Google docs files at HTML.

When exported, files containing links have their `href` attributes set to a Google URL with tracking parameters.  When the reader clicks one of these links they are taken to a Google page that tells them they are being redirected, and can then click a button to go to the intended destination.

This utility removes that behavior and replaces `href` attributes with the actual link that the document author wanted the reader to go to.

## Setup

```
$ npm install
```

## Usage

```
$ npm start <filename>
```

Where `<filename>` should be the name of a file in the same directory as this utility is in.

It will write a corrected version of the file to `fixed_<filename>`, also in the same directory as the utility is in.  The original file `<filename>` remains unchanged.

Example output:

```
$ npm start 3DataStructures.html

> google-doc-link-fix@0.0.1 start /Users/simon/source/projects/google-doc-link-fix
> node index.js -- "3DataStructures.html"

Wrote: fixed_3DataStructures.html
```

## Example Link Transformation

For example, a link in the source document that looks like this:

```
https://www.google.com/url?q=https://redis.io/topics/data-types%23strings&amp;sa=D&amp;ust=1573152930371000
```

will be transformed to a link in the "fixed" document that looks like this:

```
https://www.google.com/url?q=https://redis.io/topics/data-types%23strings
```