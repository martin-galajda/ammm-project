const readline = require('readline')
const fs = require('fs')
const os = require('os')

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

const directoryFiles = fs.readdirSync('./')
const datFiles = directoryFiles.filter(dirFilename => dirFilename.includes('.dat'))
// rl.question()
console.log(directoryFiles)
console.log(datFiles)

const options = datFiles.map((datFilename, idx) => `>>> ${datFilename} (OPTION ${idx})${os.EOL}`)

const parseIncomp = incompStr => {
  incompStr = incompStr.replace(/  +/g, ' ');
  const incompLines = incompStr
    .split(' [')
    .filter(line => line.includes(']'))
    .map(line => line.split(']')
    .join(''))
  
  const results = []
  incompLines.forEach(incompLine => {
    results.push(incompLine.split(' '))
  })

  return results
}

const transformVariableNamesMap = {
  package_x: 'packageX',
  package_y: 'packageY',
}

const convertDatToJson = datFilename => {
  let file = fs.readFileSync(datFilename, {
    encoding: 'UTF-8'
  })

  const lines = file.split(os.EOL).filter(line => line.length && !line.includes('//'))
  file = lines.join(os.EOL)

  let variableLines = file.split(';').map(line => line.split(os.EOL).join(''))

  const variables = {}
  variableLines.forEach(variableLine => {
    let [varName, varValue] = variableLine.split('=')

    if (varValue && varValue.includes) {
      if (varName !== 'incomp' && varValue.includes('[')) {
        varValue = varValue.replace('[', '').replace(']', '').split(' ')
      }  
      
      variables[varName] = varValue
    }
  })

  variables.incomp = parseIncomp(variables.incomp)

  // console.log(file)
  console.log(variables)
  return variables
}

rl.question(`Which of the files you want to convert from dat to json? Enter number:${os.EOL}${options}`, answer => {
  console.log(`You answered ${answer}`)

  const datFilename = datFiles[answer]
  const variables = convertDatToJson(datFilename)

  Object.keys(transformVariableNamesMap).forEach(variableNameKey => {
    variables[transformVariableNamesMap[variableNameKey]] = variables[variableNameKey]
    delete variables[variableNameKey]
  })

  Object.keys(variables).forEach(variableKey => {
    const variable = variables[variableKey] 
    if (typeof(variable) == 'string') {
      variables[variableKey] = Number(variable)
    } else {
      if (typeof(variable[0]) == 'string') {
        variables[variableKey] = variable.map(elem => Number(elem))
      } else {
        variables[variableKey] = variable.map(elem => elem.map(elem2 => Number(elem2)))
      }
    }
  })

  console.log(variables)

  const jsonFilename = datFilename.replace('.dat','.json')
  fs.writeFileSync(jsonFilename, JSON.stringify(variables, null, '\t'))

  rl.close()
})