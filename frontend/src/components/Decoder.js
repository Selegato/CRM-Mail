import { useEffect, useState } from 'react';
import { decode } from 'js-base64';


//funcao que decodifica o payload
const useDecodedPayload = () => {
    const [decodedPayload, setDecodedPayload] = useState({
        //dados do payload
        tenantId: '',
        title: undefined,
        alertSuccessMessage: '',
        alertErrorMessage: '',
        documentNumber: '',
        name: '',
        lastName: '',
        email: '',
        phone: '',
        celPhone: '',
        isPrime: false,
        isMobile: false,
        primaryColor: ''
    });

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const payload = urlParams.get("payload");
        if (payload) {
            try {
                const payloadDecoded = JSON.parse(decode(payload));
                // verifica se celphone nao e vazio ou undef, remove +55 caso tenha
                if (payloadDecoded.celPhone && payloadDecoded.celPhone.startsWith('+55')) {
                    payloadDecoded.celPhone = payloadDecoded.celPhone.slice(3);
                }
                // atualiza o estado com os dados do payload
                setDecodedPayload(payloadDecoded);
            } catch (error) {
                console.error("Error to decode payload", error);
            }
        }
    }, []);

    return decodedPayload;
};

export default useDecodedPayload;