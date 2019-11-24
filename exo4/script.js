//Parcours de fichier
'use strict';
let fs = require('fs');
let path = require('path');
let process = require("process");

let paths = '/Users/yassineel-azami/Downloads/Corpus_detourage/'
let dir= paths+"html/";
let outDir= paths+"UF/";

let extractor = require('unfluff');

//extractor = require('unfluff');

let rawdata = fs.readFileSync(paths+'doc_lg.json');
let objs = JSON.parse(rawdata);




for (var key in objs){
	var file = key;
	var lg = objs[key];
	// console.log(f);
	var langue = "";
	switch(lg){
		case "Greek": langue = "el";
			break;
		case "Polish": langue = "pl";
			break;
		case "Russian": langue = "ru";
			break;
		case "Chinese": langue = "zh";
			break;
		default: langue = "en";
			break;
	}

	try {
		if (fs.existsSync(path.join(dir,file))){
			fs.readFile(path.join(dir,file), 'utf-8', (err, data) => {
				if (err) throw err;
				var content = extractor(data,langue);


				fs.writeFile(path.join(outDir,file), content.text,'utf-8', (err) => {
					if (err) throw err;
				})
			})
		}
	} catch(err) {
		console.error(err)
	}


}