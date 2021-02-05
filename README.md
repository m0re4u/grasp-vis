# grasp-vis
Visualization of NAF files. Built using Flask, jQuery and `D3.js`.
Information being displayed is:
- Raw text
- Events detected
- Factuality information about the events
- SRL using events as predicates

## Installation
- Install requirements in `requirements.txt`
- Get some NAF files to visualize.
- `python3 -m flask run`

## TODO
### Definitely
- [x] Keep event highlighted in text when clicked
- [x] Add role spans to graph
- [ ] Hover over role -> highlight in text
