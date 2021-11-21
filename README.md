# Unnatural language generation

CLI tool to generate random gibberish texts based on markov chains.

## Usage

### Process text

`ulg process --json <graph dump> --input <text file> --output <output file> --order <order>`

* `graph dump` - json file of your graph
* `text file` - text file you want to process
* `output file` - json file where new graph will be stored
* `order` - markov chain order

### Generate text

`ulg generate --json <graph dump> --order <order> --words <words>`

* `graph dump` - json file of your graph
* `order` - markov chain order
* `words` - number of words to generate

## Credits

Thanks to [@danbst](https://github.com/danbst) for the idea
