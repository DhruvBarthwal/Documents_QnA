const BASE_URL = "http://localhost:8000";

export async function uploadfile(file: File){
    const formData = new FormData();
    formData.append("file",file)

    const res = await fetch(`${BASE_URL}/upload`,{
        method : "POST",
        body : formData,
    });

    if (!res.ok) throw new Error("Upload Faild");
    return res.json();
}

export async function askQuestion(query : string){
    const res = await fetch(`${BASE_URL}/ask?query=${encodeURIComponent(query)}`,
        {method : "POST"}
    )
    if(!res.ok) throw new Error("Query failed")
        return res.json();
}