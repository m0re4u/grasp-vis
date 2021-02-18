# grasp-vis
Visualization of NAF and TRiG files. Built using Flask, jQuery and `D3.js`.

Information being displayed is:
- Raw text
- Events detected
- Factuality information about the events
- SRL using events as predicates
- Graph containing raw RDF triplets. Red nodes denote mentions in the text. Black nodes are all other types of nodes. Link types are not shown yet. You can zoom (by scrolling up and down) and move around (click+drag) in the RDF visualization box.

It is recommended to visualize the `small_` versions of the files, which show heavily (randomly) truncated versions of the original RDF files.

## Installation
- Install requirements in `requirements.txt`
- Create `.env` file in the project directory, with the following contents:
```
export APP_SETTINGS="config.DevelopmentConfig"
```
- `source initialize.sh` to setup environment variables.
- Run `python3 -m flask run`

## Data
The provided data are two articles from public articles on vaccination. They are part of the [vaccination corpus](https://vaccinationcorpus.wordpress.com/).
