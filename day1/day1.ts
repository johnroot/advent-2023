import * as fsPromise from 'fs/promises';

const part1 = /\d/g
const part2 = /(?=(one|two|three|four|five|six|seven|eight|nine|\d))/g
let sum = 0;

function castToIntString(digit: string) {
    const parsed = parseInt(digit)
    if (!Number.isNaN(parsed)) {
        return digit
    }

    switch(digit) {
        case "one":
            return "1";
        case "two":
            return "2";
        case "three":
            return "3";
        case "four":
            return "4";
        case "five":
            return "5";
        case "six":
            return "6";
        case "seven":
            return "7";
        case "eight":
            return "8";
        case "nine":
            return "9";
        default:
            console.log(`Hm? Recieved digit value of: ${digit}`);
            return "";
    } 
}

const inputFile = await fsPromise.open(`${__dirname}/day1input.txt`);
for await (const line of inputFile.readLines()) {
    const digits = Array.from(line.matchAll(part2), (match) => match[1])
    if (!!digits) {
        const firstDigit = castToIntString(digits[0])
        const lastDigit = castToIntString(digits[digits.length - 1])
        const combined = parseInt(firstDigit + lastDigit)
        // console.log(`Turned ${line} into ${combined}`)
        sum += combined
    }
}

console.log(sum)
