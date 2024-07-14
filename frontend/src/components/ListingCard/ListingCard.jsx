import {Card, CardHeader, CardBody, Divider, CardFooter} from "@nextui-org/react";


export const ListingCard = ({ listing }) => {
    return (
        // Probably want to add a link to listings page here at some point
        <Card className="max-w-[400px] min-w-[400px]" data-testid="listing-card">
            <CardHeader className="flex gap-10">
                <div className="flex flex-col">
                    <p className="text-md">{listing.title}</p>
                    <p className="text-small text-default-500">Being sold by: {listing.seller.username}</p>
                </div>
            </CardHeader>
            <Divider/>
            <CardBody>
                <p>Price: ${listing.price}</p>
                <p>{listing.description}</p>
            </CardBody>
            <Divider/>
            <CardFooter>
                <p className="text-medium text-default-500">Listed: {listing.listed_date}</p>
            </CardFooter>
        </Card>
    );
}
