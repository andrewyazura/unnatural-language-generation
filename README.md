[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)

# Unnatural Language Generator

This project provides a CLi and a Python package for generating *un*natural language.
It uses Markov chains to make directed graph of words and then generates sentences.
Each edge contains `count` of how many times two nodes it connects were found in text.
During text generation `count` is used to randomly choose next word.

## Textgen CLI

CLI has two main commands: `generate` and `parse`.

```bash
$ textgen --help
Usage: textgen [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate  generate text from a graph
  parse     generate a graph from text files
```

### Parse

Parse command requires you to specify at least one text file
to process and creates a JSON-file with graph's contents.

```bash
$ textgen parse --help
Usage: textgen parse [OPTIONS]

Options:
  -in, --input FILE    text files to parse (can be repeated)  [required]
  -out, --output FILE  path to file to export graph into  [required]
  -g, --graph FILE     path to an exsiting graph file
  -o, --order INTEGER  order of graph (read README to know more)  [default: 1]
  --help               Show this message and exit.
```

### Generate

Generate command requires an exisiting JSON-file of a graph to generate
a block of text. You can specify amount of words to generate.

```bash
$ textgen generate --help
Usage: textgen generate [OPTIONS]

Options:
  -g, --graph FILE     path to the graph file  [required]
  -w, --words INTEGER  number of words to generate  [default: 255]
  -o, --order INTEGER  order of graph (read README to know more)  [default: 1]
  --help               Show this message and exit.
```

## Order

**Order** is how many words single node contains.
Increasing the order usually also increases grammatical correctness of text generated,
but it also makes it harder to generate text, since some nodes will not have outgoing edges.

For example, graph with order equal to 1 will look like this:

```
he -> is 24
he -> was 19
he -> may 5
...
may -> be 11
may -> have 2
...
```

But graph with order equal to 3 will look like this:

```
with him to -> go 5
with him to -> run 1
...
him to go -> away 3
him to go -> somewhere 1
...
```

With higher order, text will look more natural, but it will also require more input text to work.
With lower order, you can generate a lot of nonsense text.

## Credits

Thanks to [@danbst](https://github.com/danbst) for the idea.

Cool article that shows how to do the same thing: [yurichev.com](https://yurichev.com/blog/markov/)

Download `.txt` books there: [Gutenberg library](https://www.gutenberg.org/)
