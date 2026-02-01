"use client"
import { useState } from "react"
import FileUpload from "@/components/FileUpload"
import AnswerBox from "@/components/AnswerBox"
import QuestionBox from "@/components/QuestionBox"
import Navbar from "@/components/Navbar"

const page = () => {

  const [uploaded, setUploaded] = useState(false);
  const [answer, setAnswer] = useState("");
  const [latency, setLatency] = useState(0);

  return (
    <div className="bg-red-950 text-white items-center flex flex-col h-screen w-full mx auto p-6">
      <Navbar/>
      <div className="text-6xl font-bold mb-4 mt-20">
        Document Q&A
      </div>
      <FileUpload onUploaded ={()=> setUploaded(true)} />
        {
          uploaded && (
            <QuestionBox
              onAnswer = {(ans,time) => {
                setAnswer(ans)
                setLatency(time)
              }}
            />
          )
        }
        <AnswerBox answer = {answer} latency = {latency}/>
    </div>
  )
}

export default page