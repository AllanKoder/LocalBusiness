function GetInput() {
	var data = document.getElementById("data").value
	document.getElementById('TopHeadline').innerHTML = "Top Results:";

	eel.giveInput(data)(GetOutput)
}
function PrintAll(){
	eel.getCatalog()(GetOutput);

}
function GetOutput(Result){
	document.getElementById('InputResult').innerHTML = Result;

}


