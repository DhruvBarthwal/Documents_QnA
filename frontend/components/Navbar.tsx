

const Navbar = () => {
  return (
    <div className="flex p-2 w-full justify-between">
        <div className="text-xl font-bold">
            QADox
        </div>
        <div className="flex gap-15 ml-28">
            <h1 className="cursor-pointer">Home</h1>
            <h1 className="cursor-pointer">Contact</h1>
            <h1 className="cursor-pointer">Support</h1>
        </div>
        <div className="flex gap-8">
            <h1>Insta</h1>
            <h1>Discord</h1>
            <h1>Twitter</h1>
        </div>
    </div>
  )
}

export default Navbar