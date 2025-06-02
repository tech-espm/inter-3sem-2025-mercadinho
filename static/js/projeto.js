"use strict";

window._ = function (id) {
	return ((typeof id === "string") ? document.getElementById(id) : id);
};

window.encode = (function () {
	var amp = /\&/g, lt = /</g, gt = />/g, quot = /\"/g, apos = /\'/g, grave = /\`/g;
	window.encodeValue = function (x) {
		return (x ? x.replace(amp, "&amp;").replace(lt, "&lt;").replace(gt, "&gt;").replace(quot, "&#34;").replace(apos, "&#39;").replace(grave, "&#96;") : "");
	};
	return function (x) {
		return (x ? x.replace(amp, "&amp;").replace(lt, "&lt;").replace(gt, "&gt;") : "");
	};
})();

window.BlobDownloader = {
	blobURL: null,

	saveAs: (window.saveAs || window.webkitSaveAs || window.mozSaveAs || window.msSaveAs || window.navigator.saveBlob || window.navigator.webkitSaveBlob || window.navigator.mozSaveBlob || window.navigator.msSaveBlob),

	supported: (("Blob" in window) && ("URL" in window) && ("createObjectURL" in window.URL) && ("revokeObjectURL" in window.URL)),

	alertNotSupported: function () {
		Swal.error("Infelizmente seu navegador não suporta essa funcionalidade " + emoji.sad);
		return false;
	},

	download: function (filename, blob) {
		if (!BlobDownloader.supported)
			return false;
		if (BlobDownloader.blobURL) {
			URL.revokeObjectURL(BlobDownloader.blobURL);
			BlobDownloader.blobURL = null;
		}

		if (BlobDownloader.saveAs) {
			try {
				BlobDownloader.saveAs.call(window.navigator, blob, filename);
				return;
			} catch (ex) {
				Swal.error("Ocorreu um erro durante o download dos dados " + emoji.sad);
			}
		}

		var a = document.createElement("a"), evt;
		BlobDownloader.blobURL = URL.createObjectURL(blob);
		a.href = BlobDownloader.blobURL;
		a.download = filename;
		if (("MouseEvent" in window)) {
			try {
				a.dispatchEvent(new MouseEvent("click"));
				return;
			} catch (ex) {
			}
		}
		if (("createEvent" in document)) {
			try {
				evt = document.createEvent("MouseEvents");
				evt.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
				a.dispatchEvent(evt);
				return;
			} catch (ex) {
			}
		}
		a.click(); // Works on Chrome but not on Firefox...
		return true;
	}
};

window.addFilterButton = function (parent, icon, text, handler, title, btnClass) {
	var p = _(parent), label, btn, i;
	if (!p)
		return;
	label = document.createElement("label");
	btn = document.createElement("button");
	btn.setAttribute("type", "button");
	btn.className = "btn btn-sm " + (btnClass || "btn-secondary");
	i = document.createElement("i");
	i.className = "fa fa14 " + icon;
	btn.appendChild(i);
	if (text)
		btn.appendChild(document.createTextNode(text));
	if (title)
		btn.setAttribute("title", title);
	btn.onclick = handler;
	label.appendChild(btn);
	p.insertBefore(document.createTextNode(" "), p.firstChild);
	p.insertBefore(label, p.firstChild);
	return btn;
};

window.customFilterHandler = function (table, input) {
	var lastSearch = "", handler = function () {
		var s = trim(input.value.normalize()).toUpperCase();
		if (lastSearch !== s) {
			lastSearch = s;
			table.search(s).draw();
		}
		return true;
	};
	input.onchange = handler;
	input.onkeyup = handler;
};

window.customFilterHandlerPlain = function (table, input) {
	var lastSearch = "", handler = function () {
		var s = trim(input.value.normalize());
		if (lastSearch !== s) {
			lastSearch = s;
			table.search(s).draw();
		}
		return true;
	};
	input.onchange = handler;
	input.onkeyup = handler;
};

window.prepareCustomFilter = function (table, tableId, customFilterLabel, placeholder) {
	var label, input, parent = _(tableId + "_filter");
	if (parent) {
		while (parent.firstChild)
			parent.removeChild(parent.firstChild);
		label = document.createElement("label");
		label.appendChild(document.createTextNode((customFilterLabel === null || customFilterLabel === undefined) ? "Filtro:" : customFilterLabel));
		input = document.createElement("input");
		if (window.prepareCustomFilterPlain)
			customFilterHandlerPlain(table, input);
		else
			customFilterHandler(table, input);
		input.className = "form-control form-control-sm input-sm upper";
		input.setAttribute("type", "search");
		input.setAttribute("placeholder", placeholder || "");
		input.setAttribute("aria-controls", tableId);
		label.appendChild(input);
		parent.appendChild(label);
	}
};

function waitSwal() {
	Swal.fire({
		html: "Por favor, aguarde...",
		allowOutsideClick: false,
		allowEscapeKey: false,
		allowEnterKey: false,
		didOpen: () => {
			Swal.showLoading()
		}
	});
}

async function exibirErro(response) {
	let r = await response.text();

	let json = null;
	try {
		json = JSON.parse(r);
	} catch (ex) {
		// Apenas ignora...
	}

	if (json) {
		if (typeof json === "string") {
			r = json;
		} else if (json.message) {
			r = json.message;
		}
	}

	return Swal.fire("Erro", r, "error");
}
