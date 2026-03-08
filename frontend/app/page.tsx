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
    <div className="bg-gray-950 text-white items-center flex flex-col h-screen w-full mx auto p-6">
      <Navbar/>
      <div className="flex flex-col items-center mb-4 mt-20">
        <div className="text-[60px] font-bold">
          Want to Talk to Your Documents?
        </div>
        <div className="text-[30px]">
          Ask with a click, get answers quick.
        </div>
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