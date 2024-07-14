import { Image } from "@nextui-org/react";

export const NotLoggedInPage = () => {
    return (
        <div className="flex flex-col items-center" style={{backgroundColor:"dimgray"}}>
            <br/>
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
        </div>
    );
}
