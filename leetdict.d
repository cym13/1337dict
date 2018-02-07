#!/usr/bin/env rdmd

import std.algorithm;
import std.array;
import std.bigint;
import std.conv;
import std.range;
import std.stdio;
import std.traits;

immutable string[string] LetterNum, LetterSym;

shared static this() {
    LetterNum = [
      "a": "4",
      "e": "3",
      "g": "9",
      "i": "1",
      "l": "1",
      "o": "0",
      "s": "5",
      "t": "7",
    ];

    LetterSym = [
      "a": "@",
      "e": "€",
      "i": "!",
      "s": "$",
      "t": "+"
    ];
}


auto leetLetter(string letter) {
    import std.ascii: isAlpha;
    import std.string: toLower, toUpper;

    string[] result = [letter.toLower];

    if (letter[0].isAlpha)
        result ~= letter.toUpper;

    if (letter in LetterNum)
        result ~= LetterNum[letter];

    if (letter in LetterSym)
        result ~= LetterSym[letter];

    return result;
}
unittest {
    assert(leetLetter("a") == ["a", "A", "4", "@"]);
    assert(leetLetter("b") == ["b", "B"]);
    assert(leetLetter("1") == ["1"]);
    assert(leetLetter("@") == ["@"]);
}


auto leetWord(string word) {
    if (word.length == 0)
        return "";

    if (word.length == 1)
        return leetLetter(word);

    foreach (w ; leetWord(word[0..$])
        foreach (w ; leetLetter(word[$-1])
}
unittest {
    assert(leetWord("ba1:").array ==
            ["ba1:", "bA1:", "b41:", "b@1:",
             "Ba1:", "BA1:", "B41:", "B@1:"]);
}


auto genPasswords(string[] wordset,
                  uint minlen,
                  uint maxlen,
                  bool permute,
                  uint skip) {
    return cast(string[])[];
}
unittest {
    assert(genPasswords(["ba1:"], 0, 4, false, 0).array ==
            leetWord("ba1:").array);

    assert(genPasswords(["ba1:"], 0, 4, true, 0).array ==
            leetWord("ba1:").array);

    assert(genPasswords(["b", "c"], 0, 2, false, 0).array ==
            ["b", "B", "c", "C", "bc", "bC", "Bc", "BC"]);

    assert(genPasswords(["b", "c"], 0, 1, false, 0).array ==
            ["b", "B", "c", "C"]);

    assert(genPasswords(["b", "c"], 2, 2, false, 0).array ==
            ["bc", "BC", "Bc", "BC"]);

    assert(genPasswords(["b", "c"], 0, 2, true, 0).array ==
            ["b",  "B",  "c",  "C",
             "bc", "bC", "Bc", "BC",
             "cb", "cB", "Cb", "CB"]);

    assert(genPasswords(["b", "c"], 0, 2, true, 8).array ==
             ["cb", "cB", "Cb", "CB"]);
}


auto variationsNumber(string word) {
    return 0;
}
unittest {
    assert(variationsNumber("aa") == 16);
    assert(variationsNumber("a")  ==  4);
    assert(variationsNumber("b")  ==  2);
    assert(variationsNumber("1")  ==  1);
    assert(variationsNumber("@")  ==  1);
}

auto factorial(T)(T n) if (isIntegral!T) {
    return factorial(BigInt(n));
}

BigInt factorial(BigInt n)
in {
    assert(n >= 0);
}
do {
    auto i = BigInt(1);
    for (; n>1 ; n--)
        i *= n;
    return i;
}
unittest {
    assert(factorial(0) == 1);
    assert(factorial(1) == 1);
    assert(factorial(120) ==
           BigInt("66895029134491270575881180540903725867527463331380298"
                ~ "10295671352301633557244962989366874165271984981308157"
                ~ "63789321409055253440858940812185989848111438965000596"
                ~ "4960521256960000000000000000000000000000"));
}


BigInt permutationsNumber(string[] combination, bool permute) {
    return permute ? BigInt(1) : combination.length.factorial;
}
unittest {
    assert(permutationsNumber(["b", "c", "d"], false) == 1);
    assert(permutationsNumber(["b", "c", "d"], true)  == 6);
}


uint possibilitiesNumber(string[] wordset, bool permute) {
    return 0;
}
unittest {
    assert(possibilitiesNumber(["haha"],     false) == 64);
    assert(possibilitiesNumber(["bcbc"],     false) == 16);
    assert(possibilitiesNumber(["ha", "bc"], false) == 44);
    assert(possibilitiesNumber(["ha", "bc"], true)  == 76);
}


struct DropResult {
    string[][] combinations;
    uint       iteration;

    alias combinations permutations;
}

auto dropCombinations(string[] wordset, uint skip, bool permute) {
    return DropResult();
}
unittest {
    auto wordset = ["ha", "bc"];

    DropResult dropResult;

    dropResult = dropCombinations(wordset, 0, false);
    assert(dropResult.combinations.array == [["ha"], ["bc"], ["ha", "bc"]]);
    assert(dropResult.iteration == 0);

    dropResult = dropCombinations(wordset, 0, true);
    assert(dropResult.combinations.array == [["ha"], ["bc"], ["ha", "bc"]]);
    assert(dropResult.iteration == 0);

    dropResult = dropCombinations(wordset, 2, false);
    assert(dropResult.combinations.array == [["ha"], ["bc"], ["ha", "bc"]]);
    assert(dropResult.iteration == 2);

    dropResult = dropCombinations(wordset, 13, true);
    assert(dropResult.combinations.array == [["ha", "bc"]]);
    assert(dropResult.iteration == 12);
}

auto dropPermutations(string[] combination, uint skip) {
    return DropResult();
}
unittest {
    auto combination = ["ha", "bc", "de"];
    auto varnum      = variationsNumber(combination.join(""));

    DropResult dropResult;

    dropResult = dropPermutations(combination, 0);
    assert(dropResult.permutations.array ==
            [["ha", "bc", "de"], ["ha", "de", "bc"], ["bc", "ha", "de"],
             ["bc", "de", "ha"], ["de", "ha", "bc"], ["de", "bc", "ha"]]);
    assert(dropResult.iteration == 0);

    dropResult = dropPermutations(combination, varnum-1);
    assert(dropResult.permutations.array ==
            [["ha", "bc", "de"], ["ha", "de", "bc"], ["bc", "ha", "de"],
             ["bc", "de", "ha"], ["de", "ha", "bc"], ["de", "bc", "ha"]]);
    assert(dropResult.iteration == varnum-1);

    dropResult = dropPermutations(combination, varnum+1);
    assert(dropResult.permutations.array ==
            [                    ["ha", "de", "bc"], ["bc", "ha", "de"],
             ["bc", "de", "ha"], ["de", "ha", "bc"], ["de", "bc", "ha"]]);
    assert(dropResult.iteration == varnum-1);
}

void main(string[] args) {
    import std.stdio;
}
