const getDataElement = () => document.getElementById('data');
const normalizeSpaces = text => text.replace(/\s+/g, ' ').trim();

const toUpperCase = () => {
    const dataElement = getDataElement();
    if (dataElement) {
        dataElement.value = normalizeSpaces(dataElement.value).toUpperCase();
    }
};

const toLowerCase = () => {
    const dataElement = getDataElement();
    if (dataElement) {
        dataElement.value = normalizeSpaces(dataElement.value).toLowerCase();
    }
};

const toProperCase = () => {
    const dataElement = getDataElement();
    if (dataElement) {
        dataElement.value = normalizeSpaces(dataElement.value)
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join(' ');
    }
};

const toSentenceCase = () => {
    const dataElement = getDataElement();
    if (dataElement) {
        dataElement.value = dataElement.value
            .split('.')
            .map(word => normalizeSpaces(word))
            .map(sentence => sentence.charAt(0).toUpperCase() + sentence.slice(1).toLowerCase())
            .join('. ').trim();
    }
};

const downloadFile = () => {
    const dataElement = getDataElement();
    if (!dataElement) return;

    const blob = new Blob([dataElement.value], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'text.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};

document.getElementById('upper-case')?.addEventListener('click', toUpperCase);
document.getElementById('lower-case')?.addEventListener('click', toLowerCase);
document.getElementById('proper-case')?.addEventListener('click', toProperCase);
document.getElementById('sentence-case')?.addEventListener('click', toSentenceCase);
document.getElementById('save-text-file')?.addEventListener('click', downloadFile);
