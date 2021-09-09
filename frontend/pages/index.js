import Head from "next/head";
import Image from "next/image";
// import styles from '../styles/Home.module.css'
import Card from "../components/cards/Card";
import { useEffect } from "react";
import Cookies from "universal-cookie";
import Navbar from "../components/Navbars/Navbar";

export default function Home() {

  const cookies = new Cookies();

  // useEffect(() => {
  //   setTokenInfo({
  //     access_token: cookies.get("access_token"),
  //     token_type: cookies.get("token_type"),
  //   });
  // }, [cookies]);


  useEffect( async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_RESTAPI_URL}api/v1/users/get-info`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `${cookies.get("token_type")} ${cookies.get("access_token")}`,
        }
      }).then((res) => {
        if(res.status === 401) {
          alert("Token not valid");
        }
      })
      console.log(res.json())
      // return res.json()
  }, [])


  return (
    <div className="layout-container">
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Navbar />
      <div className="main-section flex justify-center items-center">
        <h1 className="text-3xl">Amechii</h1>
      </div>
    </div>
  );
}
