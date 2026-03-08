import { FaInstagram } from "react-icons/fa";
import { FaDiscord } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";

const Navbar = () => {
  return (
    <div className="flex p-2 w-full justify-between">
        <div className="text-xl font-bold">
            QADox
        </div>
        <div className="flex gap-15 pr-5 ml-28">
            <h1 className="cursor-pointer">Home</h1>
            <h1 className="cursor-pointer">Contact</h1>
            <h1 className="cursor-pointer">Support</h1>
        </div>
        <div className="flex gap-8">
            <h1><FaInstagram size={25} /></h1>
            <h1><FaDiscord size={25}/></h1>
            <h1><FaXTwitter size={25} /></h1>
        </div>
    </div>
  )
}

export default Navbar