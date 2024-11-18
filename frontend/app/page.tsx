"use client";

import Image from "next/image";
import { useState } from "react";

export default function SearchPage() {
  // State variables for dropdowns and input field
  const [searchType, setSearchType] = useState("Hashtag");
  const [searchDegree, setSearchDegree] = useState("Light");
  const [searchDepth, setSearchDepth] = useState("0");
  const [searchInput, setSearchInput] = useState("");
  const [platform, setPlatform] = useState("Instagram"); // New state for platform

  const handleSubmit = async () => {
    const requestData = {
      searchType: searchType,        // These names must match what your backend expects
      degreeOfSearch: searchDegree,  // (e.g., searchType, degreeOfSearch, depthOfSearch, platform, data)
      depthOfSearch: searchDepth,
      data: searchInput,
      platform: platform,
    };

    console.log("Sending data to backend:", requestData);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),  // Convert the request data to JSON format
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Response from backend:", result);
      } else {
        console.error("Error response from backend:", response.statusText);
      }
    } catch (error) {
      console.error("Error during API request:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-1 bg-[url('gradient2.avif')] bg-cover bg-center ">
      <div className="bg-[#e6e7e9d6] p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center text-[rgb(0,0,0)]">
          Social Media Search
        </h1>
        <Image
          src="/emgoa.png"
          alt="Goa"
          width={200}
          height={200}
          className="mx-auto"
        />

        {/* Dropdown for Search Type */}
        <div className="mb-4">
          <label className="block text-sm font-semibold text-black">
            Search Type
          </label>
          <select
            value={searchType}
            onChange={(e) => setSearchType(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border text-black border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-black focus:border-indigo-500"
          >
            <option value="Hashtag" font-semibold className="text-black">
              Hashtag
            </option>
            <option value="User" className="text-black">
              User
            </option>
            <option value="Link" className="text-black">
              Link
            </option>
          </select>
        </div>

        {/* Dropdown for Degree of Search */}
        <div className="mb-4">
          <label className="block text-sm font-semibold text-black">
            Degree of Search
          </label>
          <select
            value={searchDegree}
            onChange={(e) => setSearchDegree(e.target.value)}
            className="mt-1 block w-full text-black px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="Light" className="text-black">
              Light
            </option>
            <option value="Deep" className="text-black">
              Deep
            </option>
          </select>
        </div>

        {/* Dropdown for Depth of Search */}
        <div className="mb-4">
          <label className="block text-sm font-semibold text-black">
            Depth of Search
          </label>
          <select
            value={searchDepth}
            onChange={(e) => setSearchDepth(e.target.value)}
            className="mt-1 block w-full text-black px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="0" className="text-black">
              0
            </option>
            <option value="1" className="text-black">
              1
            </option>
            <option value="2" className="text-black">
              2
            </option>
          </select>
        </div>

        {/* Dropdown for Platform */}
        <div className="mb-4">
          <label className="block text-sm font-semibold text-black">
            Platform
          </label>
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            className="mt-1 block w-full text-black px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="Instagram" className="text-black">
              Instagram
            </option>
            <option value="Twitter" className="text-black">
              Twitter
            </option>
          </select>
        </div>

        {/* Input Field */}
        <div className="mb-4">
          <label className="block text-sm font-semibold text-black">
            Enter Data
          </label>
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            className="mt-1 block text-black w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Enter hashtag, username or link"
          />
        </div>

        {/* Send Button */}
        <button
          onClick={handleSubmit}
          className="w-full bg-[rgb(220,225,73)] text-black font-semibold py-2 px-4 rounded-md hover:bg-[rgb(70,162,98)] hover:text-white focus:outline-none transition duration-300"
        >
          Send
        </button>
      </div>
    </div>
  );
}
