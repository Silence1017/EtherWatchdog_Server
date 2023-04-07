package com.example.ethbeijing.entity;

import lombok.Data;

import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import org.springframework.data.mongodb.core.mapping.MongoId;

import java.io.Serializable;

@Data
@Document("transaction")
public class Transaction implements Serializable {
    private static final long serialVersionUID=1L;
    @MongoId
    private String  id;
    @Field("tx_blockhash")
    private String txBlockhash;
    @Field("tx_blocknum")
    private String txBlocknum;
    @Field("tx_fromaddr")
    private String txFromaddr;
    @Field("tx_gas")
    private String txGas;
    @Field("tx_gasprice")
    private String txGasprice;
    @Field("tx_hash")
    private String txHash;
    @Field("tx_input")
    private String txInput;
    @Field("tx_nonce")
    private String txNonce;
    @Field("tx_toaddr")
    private String txToaddr;
    @Field("tx_index")
    private String txIndex;
    @Field("tx_value")
    private String txValue;
    @Field("tx_trace")
    private String txTrace;
    @Field("p1_type")
    private String p1Type;
    @Field("p2_type")
    private String p2Type;
    @Field("p3_type")
    private String p3Type;
    @Field("p4_type")
    private String p4Type;
    @Field("p5_type")
    private String p5Type;
    @Field("p6_type")
    private String p6Type;
    @Field("p7_type")
    private String p7Type;
    @Field("p8_type")
    private String p8Type;
    @Field("re_contractaddress")
    private String reContractaddress;
    @Field("re_cumulativegasused")
    private String reCumulativegasused;
    @Field("re_gasused")
    private String reGasused;
    @Field("re_status")
    private String reStatus;
}
