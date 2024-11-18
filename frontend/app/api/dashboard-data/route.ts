// app/api/dashboard-data/route.ts
import { link } from "fs";
import { NextResponse } from "next/server";

export async function GET() {
  // Mock data or actual data fetching from a database
  const data = [
    {
      usernameOrHashtag: "aurangzeb_alamgir.ra",
      type: "Post",
      briefContent: "Auranga tatte kisi kaam ki nayi woh to tabhi marna chahiye taa...",
      link: "https://www.instagram.com/aurangzeb_alamgir.ra/",
    },
    {
      usernameOrHashtag: "#hsluts4mstuds",
      type: "Comment",
      briefContent: "Grm bshrm sanskari ao Call pr garmi nikl du zlil krke jannt ka mza dunga rgdkr",
      link: "https://www.instagram.com/khan_baba_pthan/",
    },
    
  ];

  return NextResponse.json(data);
}
