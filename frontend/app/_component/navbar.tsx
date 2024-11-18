import Image from "next/image";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-[rgb(41,111,45)] shadow-md bg-cover bg-center border border-white border-b-1 border-t-0 border-l-0 border-r-0">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Left Side: Logo */}
          <div className="flex items-center space-x-2">
            <Link href="/">
              <Image
                className="h-10 w-10"
                src="/emgoa.png"
                alt="Your Logo"
                width={20}
                height={20}
              />
            </Link>
            <span className="text-[rgb(220,225,73)] font-bold text-xl">SOCIAL MEDIA MONITORING</span>
          </div>

          {/* Right Side: Navigation Links */}
          <div className="flex space-x-6">
            {/* Search Button */}
            <Link
              href="/"
              className="text-white bg-[#fbfbf748]  hover:bg-[rgb(70,162,98)] hover:text-white px-4 py-2 rounded-md text-xl font-bold transition duration-300"
            >
              Search
            </Link>

            {/* Dashboard Button */}
            <Link
              href="/dashboard"
              className="text-white bg-[#fbfbf748] hover:bg-[rgb(70,162,98)] hover:text-white px-4 py-2 rounded-md text-xl font-semibold transition duration-300"
            >
              Dashboard
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
