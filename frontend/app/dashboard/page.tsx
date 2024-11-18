"use client"; 

import { log } from "console";
import { useState, useEffect } from "react";

interface DashboardData {
  _id: string;
  comment: string;
  profileLink: string;
  username: string;
  
}

export default function DashboardPage() {
  // State to store the data from the backend
  const [data, setData] = useState<DashboardData[]>([]);

  // Fetch the data from backend (you can replace the API with your own)
  useEffect(() => {
    async function fetchData() {
      console.log("Fetching data from backend...");
      // Replace this with your backend API call
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/fetch-all`);
      const result = await response.json();
      console.log("Data from backend:", result);
      setData(result);
    }
    fetchData();
  }, []);

  return (
    <div className="flex flex-col items-center min-h-screen p-8 bg-[url('gradient2.avif')] bg-cover bg-center">
      {/* Dashboard Container */}
      <div className="bg-[#26ed2947] p-6 min-h-screen rounded-lg shadow-lg w-full max-w-8xl">
        {/* Dashboard Header */}
        {/* <h1 className="text-3xl font-bold mb-8 text-center text-gray-900">
          Dashboard ko highlight karo in navbar with hover colors and do the same for search
        </h1> */}

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="min-w-full table-auto border-collapse">
            <thead className="bg-[rgba(233,236,234,0.81)] text-[rgb(0,0,0)] sticky top-0 ">
              <tr>
                <th className="px-6 py-3 border text-left font-semibold w-1">
                  Username/Hashtag
                </th>
                <th className="px-6 py-3 border text-left font-semibold w-1">
                  (Post/Comment)
                </th>
                <th className="px-6 py-3 border text-left font-semibold ">
                  Brief Content
                </th>
                <th className="px-6 py-3 border text-left font-semibold w-40">
                  Link
                </th>
              </tr>
            </thead>
            <tbody>
              {data.length > 0 ? (
                data.map((item, index) => (
                  <tr key={index} className="border-b">
                    <td className="px-6 py-4 text-white border">
                      {item.username}
                    </td>
                    <td className="px-6 py-4 text-white border">
                      Comment
                    </td>
                    <td className="px-6 py-4 text-white border">
                      {item.comment}
                    </td>
                    <td className="px-6 py-4 border">
                      <a
                        href={item.profileLink}
                        className="text-indigo-600 hover:underline"
                      >
                        {item.profileLink}
                      </a>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={4} className="text-center py-6 text-white">
                    No data available.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}