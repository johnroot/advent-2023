import { readFile } from 'fs/promises';

const digit = /\d/;
const validSymbol = /[^\d\.\n]/;
const gear = /\*/g;

const engineLines = (await readFile(`${__dirname}/input.txt`, 'utf8')).split('\n');
let part1Answer = 0;

let gears = new Map<string, number[]>();

function testPartNumber(row: number, numStart: number, numEnd: number) {
    const minRow = Math.max(row - 1, 0);
    const maxRow = Math.min(row + 1, engineLines.length - 1);
    const minColumn = Math.max(numStart - 1, 0);

    const engineSlice = Array.from({ length: maxRow - minRow + 1 }, (v, k) => k + minRow)
        .map(r => engineLines[r].slice(minColumn, numEnd + 2))
        .join('\n')

    if (validSymbol.test(engineSlice)) {
        const partNumber = parseInt(engineLines[row].slice(numStart, numEnd + 1))
        part1Answer += partNumber

        if (new RegExp(gear).test(engineSlice)) {
            const gearIndices = [...engineSlice.matchAll(new RegExp(gear))]
                .map(a => a.index!!);

            const sliceLength = engineSlice.split('\n')[0].length + 1

            gearIndices.forEach(i => {
                const gearRow = Math.floor(i / sliceLength) + minRow
                const gearColumn = (i % sliceLength) + minColumn
                const gearId = `${gearRow},${gearColumn}`;

                if (gears.has(gearId)) {
                    gears.get(gearId)!!.push(partNumber)
                } else {
                    gears.set(gearId, [partNumber])
                }
            });
        }
    }
}

for (let row = 0; row < engineLines.length; row++) {
    let numStart: number | null = null;
    let numEnd: number | null = null;
    for (let column = 0; column < engineLines[0].length; column++) {
        if (digit.test(engineLines[row][column])) {
            if (numStart == null) {
                numStart = column;
            }
            numEnd = column;

            if (column == engineLines[0].length - 1) {
                testPartNumber(row, numStart, numEnd);
            }
        } else {
            if (numStart != null && numEnd != null) {
                testPartNumber(row, numStart, numEnd);
            }
            numStart = numEnd = null;
        }
    }
}

const part2Answer = [...gears.values()]
    .filter(array => array.length == 2)
    .map(array => array[0] * array[1])
    .reduce((x, y) => x + y, 0)

console.log(`Part 1: ${part1Answer}`)
console.log(`Part 2: ${part2Answer}`)
