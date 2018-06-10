const fs = require('fs')
const rl = require('readline')
const os = require('os')

const ask = rl.createInterface({
  input: process.stdin,
  output: process.stdout,
})

const TRUCK_WIDTH = 12
const TRUCK_HEIGHT = 10
const TRUCK_CAPACITY = 500
const MIN_PACKAGE_PERCENTAGE_SIZE = 0.2

const freshNewTruck = () => {
  const truckPointsFree = {}
  for (let i = 0; i < TRUCK_HEIGHT; i++) {
    // new row
    truckPointsFree[i] = {}
    for (let j = 0; j < TRUCK_WIDTH; j++) {
      // for every element in line enter true 
      truckPointsFree[i][j] = true
    }
  }

  return truckPointsFree
}

const tryAssignPackage = (truckPointsFree, package) => {
  const width = package.width
  const height = package.height 
  let solutionFound = false 
  let solutionStartX = null
  let solutionStartY = null

  for (let xStartOffset = 0; (xStartOffset < TRUCK_WIDTH && !solutionFound); xStartOffset++) {
    for (let yStartOffset = 0; (yStartOffset < TRUCK_HEIGHT && !solutionFound); yStartOffset++) {
      let canBeAssigned = true
      for (let x = xStartOffset; (x < (xStartOffset + width)) && canBeAssigned; x++) {
        for (let y = yStartOffset; (y < (yStartOffset + height)) && canBeAssigned; y++) {
          if (x >= TRUCK_WIDTH || y >= TRUCK_HEIGHT) {
            canBeAssigned = canBeAssigned && false
            continue
          }

          if (!truckPointsFree[y][x]) {
            canBeAssigned = canBeAssigned && false
          }
        }
      }
      
      if (canBeAssigned) {
        console.log(`Assigning to ${xStartOffset}, ${yStartOffset}, with width ${width}, height ${height}`)
        solutionFound = true 
        solutionStartX = xStartOffset
        solutionStartY = yStartOffset
      }
    }
  }

  if (!solutionFound) {
    return null
  }


  console.log(`Setting (${solutionStartX},${solutionStartY}) as start`)
  for (let x = solutionStartX; x < solutionStartX + width; x++) {
    for (let y = solutionStartY; y < solutionStartY + height; y++) {
      truckPointsFree[y][x] = false
      // console.log(`Setting (${y},${x}) to false`)
    }
  }

  // console.log('Found solution')
  // console.log(solutionStartX)
  // console.log(solutionStartY)

  return truckPointsFree
}

const generatePackage = (maxHeight, maxWidth) => {
  return {
    width: Math.floor(Math.max(Math.floor(Math.random() * (maxWidth -1)), MIN_PACKAGE_PERCENTAGE_SIZE * maxWidth)),
    height: Math.floor(Math.max(Math.floor(Math.random() * (maxHeight -1)), MIN_PACKAGE_PERCENTAGE_SIZE * maxHeight)),
  }
}

const assignWeights = (trucks, maxCapacityTruck) => {
  trucks.forEach(truck => {
    let maxCapacityOne = maxCapacityTruck - truck.packages.length - 1
    truck.packages.forEach(package => {
      package.weight = Math.max(Math.floor(Math.random() * maxCapacityOne), 1)
      maxCapacityOne -= package.weight
    })
  })
}

const generateData = packagesToGenerate => {
  let lastTruckPointsFree = freshNewTruck()
  const packages = []
  let trucksLen = 1
  let trucks = [{
    packages: [],
  }]

  while (packagesToGenerate > 0) {
    const newPackage = generatePackage(TRUCK_HEIGHT, TRUCK_WIDTH)
    lastTruckPointsFree = tryAssignPackage(lastTruckPointsFree, newPackage)

    if (!lastTruckPointsFree) {
      trucks.push({
        packages: [],
      })
      trucksLen += 1
      lastTruckPointsFree = freshNewTruck()
      const sndAssigned = tryAssignPackage(lastTruckPointsFree, newPackage)
    }

    trucks[trucksLen - 1].packages.push(newPackage)
    packagesToGenerate -= 1
  }

  assignWeights(trucks, TRUCK_CAPACITY)
  console.log(`t length = ${trucks.length}`)

  return trucks
}

const writeGenerated = trucks => {
  const packages = []
  trucks.forEach(truck => {
    truck.packages.forEach(package => {
      packages.push(package)
    })
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

  const date = new Date()
  const timestamp = date.getTime()
  fs.writeFileSync(`./generated/generated-data-${timestamp}_p${packages.length}.dat`, output)

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
  // fs.writeFileSync(`generated-data-${timestamp}_p${packages.length}.json`, JSON.stringify(jsonOutput, null, '\t'))

}

ask.question(`How many packages do you want to generate?${os.EOL}>>> `, answer => {
  const trucks = generateData(answer)
  writeGenerated(trucks)

  ask.close()
})