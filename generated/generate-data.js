const os = require('os')
const fs = require('fs')

const NUMBER_OF_TRUCKS = 10

const MIN_HEIGHT_TRUCK = 8
const MIN_WIDTH_TRUCK = 8

const MAX_HEIGHT_TRUCK = 10
const MAX_WIDTH_TRUCK = 12

const trucks = []
let packages = []

const TRUCK_CAPACITY = 500

const CHANCE_TO_GENERATE_PACKAGE = 0.78

const TRUCK_HEIGHT = Math.min(Math.round((Math.random() * 100) % MAX_HEIGHT_TRUCK) + MIN_HEIGHT_TRUCK, MAX_HEIGHT_TRUCK)
const TRUCK_WIDTH = Math.min(Math.round ((Math.random() * 100) % MAX_WIDTH_TRUCK) + MIN_WIDTH_TRUCK, MAX_WIDTH_TRUCK)

const generateTruck = () => ({
  packages: [],
})

const generatePackages = truck => {
  let heightLeftForPackagesToGenerate = TRUCK_HEIGHT - 1
  let capacityLeft = TRUCK_CAPACITY - (Math.floor(TRUCK_CAPACITY / TRUCK_HEIGHT))

  while (heightLeftForPackagesToGenerate > 0) {
    const shouldGeneratePackage = Math.random() <= CHANCE_TO_GENERATE_PACKAGE

    const maxHeightDimension = heightLeftForPackagesToGenerate + 1
    const currentHeight = Math.max(Math.round((Math.random() * 100 ) % maxHeightDimension), 1)

    if (shouldGeneratePackage) {

      const weight = Math.max( Math.floor((Math.random() * TRUCK_CAPACITY) % capacityLeft), 1)
      capacityLeft -= weight
      capacityLeft = Math.max(capacityLeft, 1)


      truck.packages.push({
        width: Math.max( Math.floor((Math.random() * 100) % TRUCK_WIDTH), 1),
        height: currentHeight,
        // weight: Math.max( Math.floor(TRUCK_CAPACITY /  TRUCK_HEIGHT - 1), 1),
        weight: weight,
      })
    }

    heightLeftForPackagesToGenerate -= currentHeight
  }

  return truck.packages
}

for (let i = 0; i < NUMBER_OF_TRUCKS; i++) {
  trucks.push(generateTruck())
}

trucks.forEach(truck => {
  const newPackages = generatePackages(truck)

  packages = packages.concat(newPackages)
})


const packagesX = packages.map(package => package.width).join(' ')
const packagesY = packages.map(package => package.height).join(' ')
const packagesWeight = packages.map(package => package.weight).join(' ')

const incompLine = `[${packages.map(() => 0).join(' ')}]${os.EOL}`
const incomp = `[
  ${packages.map(package => incompLine).join(' ')}
]`

const output = `
pLength=${packages.length};
tLength=${trucks.length};
capacityTruck=${TRUCK_CAPACITY};
xTruck=${TRUCK_WIDTH};
yTruck=${TRUCK_HEIGHT};

package_x=[${packagesX}];
package_y=[${packagesY}];
packageWeight=[${packagesWeight}];

incomp=${incomp};
`

console.log(trucks.map(truck => truck.packages.length).join(' '))

const date = new Date()
const timestamp = date.getTime()
fs.writeFileSync(`generated-data-${timestamp}_t${NUMBER_OF_TRUCKS}.txt`, output)

const jsonOutput = {
  pLength: packages.length,
  tLength: trucks.length,
  capacityTruck: TRUCK_CAPACITY,
  xTruck: TRUCK_WIDTH,
  yTruck: TRUCK_HEIGHT,
  
  packageX: packages.map(package => package.width),
  packageY: packages.map(package => package.height),

  packageWeight: packages.map(package => package.weight),

  incomp: packages.map(() => packages.map(() => 0)),
}
fs.writeFileSync(`generated-data-${timestamp}_t${NUMBER_OF_TRUCKS}.json`, JSON.stringify(jsonOutput, null, '\t'))