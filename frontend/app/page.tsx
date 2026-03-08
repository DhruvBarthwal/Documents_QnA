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
    <div className=" relative bg-gray-950 text-white items-center flex flex-col h-screen w-full mx auto p-6 overflow-x-hidden">
      <div className="absolute -left-40 top-1/3 w-[500px] h-[450px] bg-purple-600 rounded-full blur-[180px] opacity-40"></div>

      <div className="absolute -right-40 top-1/3 w-[500px] h-[450px] bg-blue-600 rounded-full blur-[180px] opacity-40"></div>

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