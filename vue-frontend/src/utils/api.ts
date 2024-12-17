const apiCall = (type: string, path: string | URL, body: Document | XMLHttpRequestBodyInit | null | undefined, callback: { (e: any): void; (e: any): void; (e: any): void; (e: any): void; (e: any): void; (e: any): void; (arg0: string): void; }) => {
	var xobj = new XMLHttpRequest();
	xobj.open(type, path, true);
	xobj.setRequestHeader("Content-Type", "application/json");
	xobj.setRequestHeader(
		"Authorization",
		`Bearer ${localStorage.getItem("access_token")}`
	);
	xobj.send(body);
	xobj.onreadystatechange = () => {
		if (xobj.readyState == 4 && xobj.status == 200) {
			callback(xobj.responseText);
		}
	};
};

var db_url = "http://localhost:5000";

export const getAllDocuments = (callback: (arg0: []) => void) => {
    apiCall("GET", db_url + "/get_documents", null, (response) => {
        let documents = JSON.parse(response);
        callback(documents);
    });
}