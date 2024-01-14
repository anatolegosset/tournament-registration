let data;

const searchCols = ["licenceNo", "firstName", "lastName", "club"];
const numericCols = ["licenceNo", "nbPoints"];

if (hasRegistrationEnded) {
    searchCols.push("bibNo");
    numericCols.push("bibNo");
}

function onclickRow(licenceNo) {
    window.location.href = '/admin/inscrits/' + licenceNo;
}

function appendOneRow(categoryTableBody, entryObject, categoryId, searchString, classToAppend) {
    let foundStringFlag = false;
    for (let x in searchCols) {
        let colName = searchCols[x];
        let cellValue = (numericCols.includes(colName) ? entryObject[colName].toString() : entryObject[colName]).toLowerCase();
        if (cellValue.startsWith(searchString)) {
            foundStringFlag = true;
            break;
        }
    }

    if (!foundStringFlag) {
        return 0;
    }

    let entryRow = document.createElement('tr');
    entryRow.setAttribute('id', 'players-table-row-' + entryObject['licenceNo'] + '-' + categoryId);
    entryRow.setAttribute('onclick', 'onclickRow(' + entryObject['licenceNo'] + ')');
    entryRow.classList.add('players-table-row');
    entryRow.classList.add(classToAppend + '-row-' + categoryId);

    if (hasRegistrationEnded) {
        let bibNoCell = document.createElement('td');
        bibNoCell.innerHTML = entryObject['bibNo'] || '-';
        entryRow.appendChild(bibNoCell);
    }

    let licenceNoCell = document.createElement('td');
    licenceNoCell.innerHTML = entryObject['licenceNo'];
    entryRow.appendChild(licenceNoCell);

    let firstNameCell = document.createElement('td');
    firstNameCell.innerHTML = entryObject['firstName'];
    entryRow.appendChild(firstNameCell);

    let lastNameCell = document.createElement('td');
    lastNameCell.innerHTML = entryObject['lastName'];
    entryRow.appendChild(lastNameCell);

    let pointsCell = document.createElement('td');
    pointsCell.innerHTML = entryObject['nbPoints'];
    entryRow.appendChild(pointsCell);

    let clubCell = document.createElement('td');
    clubCell.innerHTML = entryObject['club'];
    entryRow.appendChild(clubCell);

    if (hasRegistrationEnded) {
        let presentCell = document.createElement('td');
        if (entryObject['markedAsPresent'] === null) {
            presentCell.innerHTML = '?';
        } else {
            presentCell.innerHTML = entryObject['markedAsPresent'] ? 'Oui' : 'Non';
        }
        entryRow.appendChild(presentCell);

        let paidCell = document.createElement('td');
        paidCell.innerHTML = entryObject['markedAsPaid'] ? 'Oui' : 'Non';
        entryRow.appendChild(paidCell);

        if (entryObject['markedAsPresent'] && !entryObject['markedAsPaid']) {
            presentCell.style.backgroundColor = '#ffcccc';
            paidCell.style.backgroundColor = '#ffcccc';
        }
    }

    let registrationDatetimeCell = document.createElement('td');
    registrationDatetimeCell.innerHTML = entryObject['registrationTime'].replace('T', ' ').slice(0, 19);
    entryRow.appendChild(registrationDatetimeCell);

    categoryTableBody.appendChild(entryRow);
    return 1;
}

function createSeparatorRow(separatorText, nbCols, categoryId, classToAppend) {
    let separatorRow = document.createElement('tr');
    let separator = document.createElement('th');
    separator.setAttribute('colspan', nbCols);
    separator.innerHTML = separatorText;
    separator.setAttribute('class', 'players-table-separator');
    separatorRow.appendChild(separator);
    separatorRow.addEventListener('click', function() {
        let rows = document.getElementsByClassName(classToAppend + '-row-' + categoryId);
        for (let i=0; i<rows.length; i++) {
            rows[i].style.display = rows[i].style.display === 'none' ? 'table-row' : 'none';
        }
    });
    return separatorRow;
}

function collapseTable(categoryId) {
    let categoryTableBody = document.getElementById('category-table-body-' + categoryId);
    let categoryColumnsHeaderRow = document.getElementById('category-columns-header-row-' + categoryId);
    if (categoryTableBody.style.display === 'none') {
        categoryTableBody.style.display = 'table-row-group';
        categoryColumnsHeaderRow.style.display = 'table-row';
    } else {
        categoryTableBody.style.display = 'none';
        categoryColumnsHeaderRow.style.display = 'none';
    }
}

const nbResults = {};

function createOneTable(categoryObject, searchString="", show=true) {
    let nbCols = hasRegistrationEnded ? 9 : 6;
    let categoryId = categoryObject['categoryId'];

    let categoryTableDiv = document.createElement('div');
    categoryTableDiv.setAttribute('class', 'category-table-div');
    categoryTableDiv.setAttribute('id', 'category-table-div-' + categoryId);

    if (!show) {
        categoryTableDiv.style.display = 'none';
    }

    let categoryTable = document.createElement('table');
    categoryTable.setAttribute('id', 'category-table-' + categoryId);
    categoryTable.setAttribute('class', 'players-table');
    categoryTableDiv.appendChild(categoryTable);

    let categoryTableHeader = document.createElement('thead');
    categoryTable.appendChild(categoryTableHeader);
    categoryTableHeader.setAttribute('onclick', 'collapseTable("' + categoryId + '")');

    let titleString;
    let columnsString;

    if (hasRegistrationEnded) {
        let nbPresentString = `Présents : ${categoryObject['presentEntryCount']}/${categoryObject['maxPlayers']}`;
        let absentString = ' (absents : ' + categoryObject['absentEntries'].length + ', ';
        let nbRegisteredString = 'inscrits : ' + categoryObject['entryCount'] + ')';
        if (categoryObject['entryCount'] > categoryObject['maxPlayers']) {
            nbRegisteredString = '<span style="color: red;">' + nbRegisteredString + '</span>';
        }

        titleString = 'Tableau ' + categoryId + ' - ' + nbPresentString + absentString + nbRegisteredString;
        titleString += "<button onclick='downloadOneCsv(\"" + categoryId + "\")'>Générer CSV</button>";

        columnsString =
            `<tr>
                <th>N° dossard</th>
                <th>N° licence</th>
                <th>Nom</th>
                <th>Prénom</th>
                <th>Points</th>
                <th>Club</th>
                <th>Présent</th>
                <th>Payé</th>
                <th>Date/heure d'inscription</th>
            </tr>`;
    } else {
        titleString = 'Tableau ' + categoryId + ' - '
        let registeredString = 'Inscrits : ' + categoryObject['entryCount'] + '/' + categoryObject['maxPlayers'];
        if (categoryObject['entryCount'] > categoryObject['maxPlayers']) {
            registeredString = '<span style="color: red;">' + registeredString + '</span>';
        }
        titleString += registeredString;
        columnsString =
        `<tr>
            <th>N° licence</th>
            <th>Nom</th>
            <th>Prénom</th>
            <th>Points</th>
            <th>Club</th>
            <th>Date/heure d'inscription</th>
        </tr>`;
    }

    let categoryInfoHeaderRow = document.createElement('tr');
    let categoryInfoHeader = document.createElement('th');
    categoryInfoHeader.setAttribute('colspan', nbCols);
    categoryInfoHeader.innerHTML = titleString;
    categoryInfoHeaderRow.appendChild(categoryInfoHeader);
    categoryTableHeader.appendChild(categoryInfoHeaderRow);

    let categoryColumnsHeaderRow = document.createElement('tr');
    categoryColumnsHeaderRow.setAttribute('id', 'category-columns-header-row-' + categoryId)
    categoryColumnsHeaderRow.innerHTML = columnsString;
    categoryTableHeader.appendChild(categoryColumnsHeaderRow);

    let categoryTableBody = document.createElement('tbody');
    categoryTableBody.setAttribute('id', 'category-table-body-' + categoryId);
    categoryTable.appendChild(categoryTableBody);

    let nbFiltered=0;

    if (categoryObject['entryCount'] <= categoryObject['maxPlayers']) {
        // If noone is absent, no need for a separator as there are no distinctions between registered players.
        if (categoryObject['absentEntries'].length > 0) {
            categoryTableBody.appendChild(createSeparatorRow('Inscrits (' + categoryObject['entries'].length + ')', nbCols, categoryId, 'entries'));
        }
        // categoryObject['entries'] contains all registered players except those who are absent.
        categoryObject['entries'].forEach(entryObject => {
            nbFiltered += appendOneRow(categoryTableBody, entryObject, categoryId, searchString, 'entries');
        });
    } else {
        categoryTableBody.appendChild(createSeparatorRow('Hors liste d\'attente (' + categoryObject['normalEntries'].length + ')', nbCols, categoryId, 'normal'));

        categoryObject['normalEntries'].forEach(entryObject => {
            nbFiltered += appendOneRow(categoryTableBody, entryObject, categoryId, searchString, 'normal');
        });

        if (categoryObject['overridenEntries'].length > 0) {
            categoryTableBody.appendChild(createSeparatorRow('Repêchés de la liste d\'attente (' + categoryObject['overridenEntries'].length + ')', nbCols, categoryId, 'overriden'));

            categoryObject['overridenEntries'].forEach(entryObject => {
                nbFiltered += appendOneRow(categoryTableBody, entryObject, categoryId, searchString, 'overriden');
            });

            categoryTableBody.appendChild(createSeparatorRow('Repoussés en liste d\'attente (' + categoryObject['squeezedEntries'].length + ')', nbCols, categoryId, 'squeezed'));

            categoryObject['squeezedEntries'].forEach(entryObject => {
                nbFiltered += appendOneRow(categoryTableBody, entryObject, categoryId, searchString, 'squeezed');
            });
        }
        categoryTableBody.appendChild(createSeparatorRow('Liste d\'attente (' + categoryObject['waitingEntries'].length + ')', nbCols, categoryId, 'waiting'));

        categoryObject['waitingEntries'].forEach(entryObject => {
            nbFiltered += appendOneRow(categoryTableBody, entryObject, categoryId, searchString, 'waiting');
        });
    }

    if (categoryObject['absentEntries'].length > 0) {
        categoryTableBody.appendChild(createSeparatorRow('Absents (' + categoryObject['absentEntries'].length + ')', nbCols, categoryId, 'absent'));

        categoryObject['absentEntries'].forEach(entryObject => {
            nbFiltered += appendOneRow(categoryTableBody, entryObject, categoryId, searchString, 'absent');
        });
    }

    nbResults[categoryId] = nbFiltered;
    document.getElementById('players-by-category-div').appendChild(categoryTableDiv);
    if (nbFiltered === 0 && searchString.length > 0) {
        return 0;
    } else {
        return 1;
    }
}

function filterData() {
    let searchString = document.getElementById('players-by-category-search').value.toLowerCase();
    document.getElementById('players-by-category-div').innerHTML = "";

    let tableSpans = Array.from(document.getElementsByClassName('show-table-span'));
    let currentDisplayed = tableSpans.filter(span => span.classList.contains('navbar-link-current'));
    let currentCategoryId = currentDisplayed.length > 0 ? currentDisplayed[0].id.replace('show-span-', '') : null;

    if (currentCategoryId === null) {
        currentCategoryId = "all";
        console.error("No category is currently displayed.");
    }

    let nbFiltered = 0;
    data.forEach(categoryObject => {
        let show = currentCategoryId == "all" || categoryObject['categoryId'] === currentCategoryId;
        nbFiltered += createOneTable(categoryObject, searchString, show);
    });
    checkIfResults(currentCategoryId);
}

function checkIfResults(categoryId=null) {
    if (categoryId === null || categoryId === "all") {
        for (let categoryId in nbResults) {
            if (nbResults[categoryId] > 0) {
                document.getElementById('no-results-p').style.display = 'none';
                return;
            }
        }

    } else {
        if (categoryId in nbResults && nbResults[categoryId] > 0) {
            document.getElementById('no-results-p').style.display = 'none';
            return;
        } else {
            document.getElementById('category-table-div-' + categoryId).style.display = 'none';
        }
    }
    document.getElementById('no-results-p').style.display = 'block';
}

function showTables(categoryId=null) {
    let tables = document.getElementsByClassName('category-table-div');
    let links = document.getElementsByClassName('show-table-span');
    if (categoryId === null) {
        for (let i=0; i<tables.length; i++) {
            tables[i].style.display = 'block';
            links[i].classList.remove('navbar-link-current');
        }
        document.getElementById("show-span-all").classList.add('navbar-link-current');
    } else {
        for (let i=0; i<tables.length; i++) {
            tables[i].style.display = 'none';
            links[i+1].classList.remove('navbar-link-current');
        }
        document.getElementById("show-span-all").classList.remove('navbar-link-current');
        document.getElementById("show-span-" + categoryId).classList.add('navbar-link-current');
        document.getElementById('category-table-div-' + categoryId).style.display = 'block';
    }
    checkIfResults(categoryId);
}


function generateCsv(categoryId) {
    if (!hasRegistrationEnded) {
        return;
    }

    let csvContent = 'data:text/csv;charset=utf-8,';
    csvContent += 'N° dossard,N° licence,Nom,Prénom,Points,Club\n';
    let csvRows = [];

    let categoryObject = data.find(categoryObject => categoryObject['categoryId'] === categoryId);

    let relevantEntries = 'entries' in categoryObject ? categoryObject['entries'] : categoryObject['normalEntries'].concat(categoryObject['overridenEntries']);

    relevantEntries.forEach(entryObject => {
        if (entryObject['markedAsPresent']) {
            let csvRow = [];
            csvRow.push(entryObject['bibNo'] || '-');
            csvRow.push(entryObject['licenceNo']);
            csvRow.push(entryObject['lastName']);
            csvRow.push(entryObject['firstName']);
            csvRow.push(entryObject['nbPoints']);
            csvRow.push(entryObject['club']);
            csvRows.push(csvRow.join(','));
        }
    });
    csvContent += csvRows.join('\n');
    console.log(csvContent);
    return csvContent;
}

function downloadOneCsv(categoryId) {
    let csvContent = generateCsv(categoryId);
    if (csvContent) {
        let encodedUri = encodeURI(csvContent);
        let link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', 'tableau_' + categoryId + '.csv');
        document.body.appendChild(link);
        link.click();
    }
}

async function downloadAll() {
    let downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', '/api/admin/csv?by_category=true');
    downloadLink.setAttribute('download', 'competiteurs_par_tableau.zip');
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

function processData() {
    let categoriesNavbar = document.getElementById('categories-navbar');

    data.forEach(categoryObject=> {
        let categoryId = categoryObject['categoryId'];

        let listElement = document.createElement('li');
        listElement.setAttribute('class', 'navbar-element');

        let linkElement = document.createElement('span');
        linkElement.setAttribute('class', 'navbar-link');
        linkElement.classList.add('show-table-span');
        linkElement.setAttribute('id', 'show-span-' + categoryId);
        linkElement.setAttribute('onclick', 'showTables("' + categoryId + '")');
        linkElement.innerHTML = categoryId;
        listElement.appendChild(linkElement);
        categoriesNavbar.appendChild(listElement);

        createOneTable(categoryObject);
    });
}

async function fetchData() {
    const start = new Date();
    let response = await fetch('/api/admin/by_category');
    if (!response.ok) {
        console.error(response.status + ' ' + response.statusText);
    } else {
        let json = await response.json();
        data = json['categories'];
        console.log(data);
        processData();
        showTables();
    }
}

document.getElementById('players-by-category-search').value = "";

document.getElementById('players-by-categories-navbar-link').setAttribute('class', 'navbar-link-current');

fetchData().then(() => {
    showContent();
});
