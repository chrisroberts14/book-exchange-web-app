import { Image, Link } from "@nextui-org/react";
import { GithubIcon } from "../icons.tsx";

export const NotLoggedInPage = () => {
    return (
        <div className="flex flex-col items-center" style={{backgroundColor:"dimgray"}}>
            <h2 className="text-3xl">You are not logged in</h2>
            <p className="text-xl">Please log in to continue</p>
            <br/>
            <Image
                width={240}
                src="../../../public/Stack_of_Books_PNG_Clipart_Image.png"
                alt="Book stack"
                className="m-5"
            />
            <h1 className="text-4xl">Book exchange</h1>
            <br/>
            <Link isExternal href="https://github.com/chrisroberts14/book-exchange-web-app">
                <GithubIcon className="text-default-100" size="50"/>
            </Link>
            <br/>
        </div>
    );
}
